from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
from administration.models import FinancialFee, User
from django.conf import settings


class Command(BaseCommand):
    help = 'Entrena un modelo de predicción de riesgo de morosidad basado en datos históricos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando entrenamiento del modelo de riesgo de morosidad...'))
        
        try:
            # 1. Obtener todos los registros de FinancialFee
            financial_fees = FinancialFee.objects.all().select_related('unit', 'unit__owner')
            
            if financial_fees.count() < 10:
                self.stdout.write(
                    self.style.WARNING('⚠️ Insuficientes datos para entrenar el modelo (mínimo 10 registros). '
                                     'Creando datos sintéticos para demostración...')
                )
                # Crear algunos datos sintéticos para demostración
                self._create_synthetic_data()
                financial_fees = FinancialFee.objects.all().select_related('unit', 'unit__owner')
            
            # 2. Crear DataFrame con las características
            data = []
            for fee in financial_fees:
                if fee.unit and fee.unit.owner:
                    # Contar pagos anteriores vencidos del mismo residente
                    previous_overdue = FinancialFee.objects.filter(
                        unit__owner=fee.unit.owner,
                        status='Vencido',
                        created_at__lt=fee.created_at
                    ).count()
                    
                    # Contar total de pagos anteriores
                    previous_total = FinancialFee.objects.filter(
                        unit__owner=fee.unit.owner,
                        created_at__lt=fee.created_at
                    ).count()
                    
                    # Calcular tasa de morosidad histórica
                    historical_default_rate = previous_overdue / max(previous_total, 1)
                    
                    # Días desde la fecha de vencimiento
                    days_since_due = (timezone.now().date() - fee.due_date).days if fee.due_date else 0
                    days_since_due = max(0, days_since_due)  # No valores negativos
                    
                    data.append({
                        'amount': float(fee.amount),
                        'historical_default_rate': historical_default_rate,
                        'previous_overdue_count': previous_overdue,
                        'days_since_due': days_since_due,
                        'is_overdue': 1 if fee.status == 'Vencido' else 0
                    })
            
            if len(data) < 10:
                self.stdout.write(
                    self.style.ERROR('❌ No hay suficientes datos válidos para entrenar el modelo.')
                )
                return
                
            df = pd.DataFrame(data)
            self.stdout.write(f'📊 Datos recopilados: {len(df)} registros')
            
            # 3. Preparar features (X) y target (y)
            X = df[['amount', 'historical_default_rate', 'previous_overdue_count', 'days_since_due']]
            y = df['is_overdue']
            
            # Verificar que tenemos casos positivos y negativos
            unique_classes = y.nunique()
            overdue_count = y.sum()
            not_overdue_count = len(y) - overdue_count
            
            self.stdout.write(f'📊 Distribución de clases: Morosos={overdue_count}, No morosos={not_overdue_count}')
            
            # Si no tenemos suficiente variabilidad o datos, generar datos sintéticos
            if unique_classes < 2 or len(df) < 50 or min(overdue_count, not_overdue_count) < 2:
                self.stdout.write(
                    self.style.WARNING('⚠️ Generando datos sintéticos para mejorar el entrenamiento...')
                )
                
                # Generar datos sintéticos más realistas
                import numpy as np
                np.random.seed(42)
                synthetic_data = []
                
                # Generar 200 registros sintéticos balanceados
                for i in range(200):
                    # Generar montos realistas
                    amount = np.random.normal(45000, 15000)
                    amount = max(amount, 10000)  # Mínimo $10k
                    
                    # Características correlacionadas de manera más realista
                    previous_overdue = np.random.poisson(0.8)
                    
                    # Días desde vencimiento (más realista)
                    if np.random.random() < 0.6:  # 60% no tienen días vencidos
                        days_since_due = 0
                    else:
                        days_since_due = np.random.exponential(12)
                    
                    # Tasa histórica basada en comportamiento anterior
                    historical_rate = min(0.7, previous_overdue * 0.12 + np.random.normal(0.25, 0.1))
                    historical_rate = max(0.0, historical_rate)
                    
                    # Lógica de morosidad más balanceada (aproximadamente 35% morosos)
                    risk_factors = 0
                    if amount > 60000:
                        risk_factors += 0.2
                    if previous_overdue > 1:
                        risk_factors += 0.3
                    if historical_rate > 0.4:
                        risk_factors += 0.3
                    if days_since_due > 15:
                        risk_factors += 0.4
                    
                    # Añadir aleatoriedad
                    risk_factors += np.random.normal(0, 0.15)
                    
                    is_overdue = risk_factors > 0.35
                    
                    synthetic_data.append({
                        'amount': amount,
                        'historical_default_rate': historical_rate,
                        'previous_overdue_count': previous_overdue,
                        'days_since_due': days_since_due,
                        'is_overdue': 1 if is_overdue else 0
                    })
                
                # Agregar datos sintéticos
                synthetic_df = pd.DataFrame(synthetic_data)
                df = pd.concat([df, synthetic_df], ignore_index=True)
                
                # Recalcular X e y
                X = df[['amount', 'historical_default_rate', 'previous_overdue_count', 'days_since_due']]
                y = df['is_overdue']
                
                new_overdue_count = y.sum()
                new_not_overdue_count = len(y) - new_overdue_count
                self.stdout.write(f'📈 Nuevos datos: Total={len(df)}, Morosos={new_overdue_count}, No morosos={new_not_overdue_count}')
            
            # Verificación final
            if y.nunique() < 2:
                self.stdout.write(
                    self.style.ERROR('❌ Aún no hay suficiente variabilidad en los datos.')
                )
                return
            
            # 4. Dividir datos y escalar
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # 5. Entrenar el modelo
            model = LogisticRegression(random_state=42, max_iter=1000)
            model.fit(X_train_scaled, y_train)
            
            # 6. Evaluar el modelo
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            self.stdout.write(f'📈 Precisión en entrenamiento: {train_score:.3f}')
            self.stdout.write(f'📈 Precisión en prueba: {test_score:.3f}')
            
            # 7. Guardar el modelo y el scaler
            model_path = os.path.join(settings.BASE_DIR, 'risk_model.joblib')
            scaler_path = os.path.join(settings.BASE_DIR, 'risk_scaler.joblib')
            
            model_data = {
                'model': model,
                'scaler': scaler,
                'feature_names': list(X.columns),
                'trained_at': timezone.now(),
                'train_score': train_score,
                'test_score': test_score
            }
            
            joblib.dump(model_data, model_path)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Modelo entrenado exitosamente y guardado en: {model_path}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'🎯 Precisión del modelo: {test_score:.3f}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante el entrenamiento: {str(e)}')
            )
            raise
    
    def _create_synthetic_data(self):
        """Crea datos sintéticos para demostración del modelo"""
        from administration.models import ResidentialUnit, FinancialFee
        from datetime import date, timedelta
        import random
        
        # Obtener usuarios existentes
        users = list(User.objects.all()[:5])  # Usar solo los primeros 5 usuarios
        
        if not users:
            self.stdout.write(self.style.ERROR('No hay usuarios en el sistema'))
            return
            
        # Crear unidades si no existen
        for i, user in enumerate(users):
            unit, created = ResidentialUnit.objects.get_or_create(
                unit_number=f'DEMO{i+1}',
                defaults={
                    'type': 'Departamento',
                    'floor': i + 1,
                    'owner': user
                }
            )
            
            # Crear cuotas históricas con diferentes estados
            base_date = date.today() - timedelta(days=180)  # 6 meses atrás
            
            for month in range(6):
                due_date = base_date + timedelta(days=30 * month)
                amount = random.uniform(200, 500)
                
                # 30% probabilidad de estar vencido
                status = 'Vencido' if random.random() < 0.3 else random.choice(['Pagado', 'Pendiente'])
                
                FinancialFee.objects.get_or_create(
                    unit=unit,
                    due_date=due_date,
                    defaults={
                        'description': f'Cuota mensual demo {due_date.strftime("%B %Y")}',
                        'amount': amount,
                        'status': status
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('✅ Datos sintéticos creados exitosamente'))