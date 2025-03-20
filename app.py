import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import random
from PIL import Image
import io
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finanzas PYMEs", layout="wide")

# Estilos CSS personalizados actualizados con mejor contraste
st.markdown("""
<style>
    /* Mejora general de contraste */
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f2f6;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FFFFFF;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #2C3038;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        border: 1px solid #3A3F48;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4FC3F7;
    }
    .metric-label {
        font-size: 1rem;
        color: #E0E0E0;
        font-weight: bold;
    }
    .metric-delta-positive {
        color: #4CAF50;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .metric-delta-negative {
        color: #F44336;
        font-size: 0.9rem;
        font-weight: bold;
    }
    
    /* Mejora del menú de navegación lateral */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1E1E1E !important;
    }
    .css-1oe6o3n {
        color: #FFFFFF !important;
    }
    .css-pkbazv {
        color: #E0E0E0 !important;
    }
    
    /* Mejora de tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2C3038;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-size: 16px;
        color: #E0E0E0;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
    
    /* Mejora de tablas */
    .dataframe {
        background-color: #2C3038 !important;
        color: #E0E0E0 !important;
    }
    .dataframe th {
        background-color: #1E88E5 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .dataframe td {
        border-color: #3A3F48 !important;
    }
    
    /* Mejora de inputs y selects */
    .stTextInput>div>div>input, .stSelectbox>div>div {
        background-color: #2C3038 !important;
        color: #E0E0E0 !important;
        border: 1px solid #3A3F48 !important;
    }
    
    /* Mejora de texto general */
    h1, h2, h3, h4, h5, h6, p, li {
        color: #E0E0E0 !important;
    }
    
    /* Mejora de iconos en el menú */
    .css-1kyxreq {
        color: #4FC3F7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Funciones de generación de datos de ejemplo
def generar_datos_mensuales(meses=12, tendencia=0.05):
    now = datetime.now()
    fechas = []
    for i in range(meses):
        fecha = now - timedelta(days=30*(meses-i-1))
        fechas.append(fecha.strftime("%b"))
    
    base_ingresos = 15000
    base_gastos = 12000
    
    ingresos = []
    gastos = []
    
    for i in range(meses):
        factor_crecimiento = (1 + tendencia) ** i
        ingresos.append(base_ingresos * factor_crecimiento * (1 + random.uniform(-0.15, 0.15)))
        gastos.append(base_gastos * factor_crecimiento * (1 + random.uniform(-0.1, 0.1)))
    
    return fechas, ingresos, gastos

def generar_transacciones(n=100):
    categorias = ["Suministros", "Alquiler", "Salarios", "Marketing", "Software", "Equipamiento", "Seguros", "Impuestos", "Otros"]
    tipos = ["Ingreso", "Gasto"]
    now = datetime.now()
    
    datos = []
    for i in range(n):
        fecha = now - timedelta(days=random.randint(0, 365))
        tipo = random.choice(tipos)
        if tipo == "Ingreso":
            categoria = "Ventas" if random.random() < 0.8 else "Otros ingresos"
            monto = random.uniform(500, 5000)
        else:
            categoria = random.choice(categorias)
            monto = random.uniform(100, 2000)
        
        datos.append({
            "fecha": fecha,
            "descripcion": f"{tipo} - {categoria}",
            "tipo": tipo,
            "categoria": categoria,
            "monto": monto
        })
    
    return pd.DataFrame(datos)

def generar_facturas(n=20):
    clientes = ["Empresa A", "Empresa B", "Empresa C", "Cliente Particular", "Negocio Local", "Corporación XYZ"]
    estados = ["Pendiente", "Pagada", "Vencida"]
    now = datetime.now()
    
    datos = []
    for i in range(1, n+1):
        fecha_emision = now - timedelta(days=random.randint(0, 90))
        vencimiento = fecha_emision + timedelta(days=30)
        estado = random.choice(estados)
        cliente = random.choice(clientes)
        monto = random.uniform(500, 8000)
        
        datos.append({
            "numero": f"F-2023-{i:03d}",
            "cliente": cliente,
            "fecha_emision": fecha_emision,
            "vencimiento": vencimiento,
            "monto": monto,
            "estado": estado
        })
    
    return pd.DataFrame(datos)

def generar_categorias_gastos():
    categorias = ["Suministros", "Alquiler", "Salarios", "Marketing", "Software", "Equipamiento", "Seguros", "Impuestos", "Otros"]
    valores = [4500, 8000, 15000, 3500, 2000, 1200, 900, 5000, 1800]
    return categorias, valores

# Sidebar para navegación
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/accounting.png", width=100)
    st.title("Navegación")
    
    opciones = st.radio(
        "Ir a:",
        ["Dashboard", "Transacciones", "Facturas", "Informes", "Configuración", "Ayuda & Soporte"]
    )
    
    st.markdown("---")
    
    # Simulación de perfil de usuario
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://img.icons8.com/color/48/000000/user-male-circle--v1.png", width=50)
    with col2:
        st.markdown("**Empresa ACME, S.L.**")
        st.markdown("*Plan Premium*")
    
    st.markdown("---")
    st.markdown("© 2023 Finanzas PYMEs")
    st.markdown("v1.0.0")

# Contenido principal
if opciones == "Dashboard":
    st.markdown("<h1 class='main-header'>Sistema de Contabilidad para PYMEs</h1>", unsafe_allow_html=True)
    
    # Tabs para diferentes vistas del dashboard
    tab1, tab2, tab3 = st.tabs(["📊 Resumen General", "💰 Flujo de Caja", "📈 Análisis"])
    
    with tab1:
        # Métricas principales
        st.markdown("<h2 class='sub-header'>Resumen Financiero</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Balance Total</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>15.243,00 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-positive'>↑ 8.5% vs. mes anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Ingresos (Mes)</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>8.759,42 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-positive'>↑ 12.3% vs. mes anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Gastos (Mes)</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>5.345,18 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-negative'>↓ -3.4% vs. mes anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Próximos Impuestos</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>2.154,33 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-positive'>Fecha límite: 20/12/2023</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Gráfico de flujo de caja mensual
        st.markdown("<h2 class='sub-header'>Flujo de Caja</h2>", unsafe_allow_html=True)
        
        meses, ingresos, gastos = generar_datos_mensuales()
        
        # Crear un dataframe para Plotly
        df_cash_flow = pd.DataFrame({
            'Mes': meses * 2,
            'Tipo': ['Ingresos'] * len(meses) + ['Gastos'] * len(meses),
            'Valor': ingresos + gastos
        })
        
        fig = px.line(df_cash_flow, x='Mes', y='Valor', color='Tipo',
                     color_discrete_map={'Ingresos': '#1E88E5', 'Gastos': '#FF5252'},
                     markers=True, title='Flujo de Caja Mensual')
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sección de facturación pendiente
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<h2 class='sub-header'>Distribución de Gastos</h2>", unsafe_allow_html=True)
            
            categorias, valores = generar_categorias_gastos()
            
            # Gráfico de pastel para categorías
            fig = px.pie(
                names=categorias,
                values=valores,
                title='Gastos por Categoría',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("<h2 class='sub-header'>Facturas Pendientes</h2>", unsafe_allow_html=True)
            
            facturas = generar_facturas()
            facturas_pendientes = facturas[facturas['estado'] == 'Pendiente'].sort_values(by='vencimiento')
            
            if not facturas_pendientes.empty:
                for _, factura in facturas_pendientes.head(5).iterrows():
                    st.markdown(f"""
                    <div class='card' style='margin-bottom: 10px; padding: 10px;'>
                        <h4 style='margin: 0;'>{factura['numero']} - {factura['cliente']}</h4>
                        <p style='margin: 5px 0;'>Monto: <b>{factura['monto']:.2f} €</b></p>
                        <p style='margin: 5px 0;'>Vence: {factura['vencimiento'].strftime('%d/%m/%Y')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No hay facturas pendientes actualmente.")
    
    with tab2:
        st.markdown("<h2 class='sub-header'>Análisis de Flujo de Caja</h2>", unsafe_allow_html=True)
        
        # Selector de periodo
        col1, col2 = st.columns([1, 2])
        with col1:
            periodo = st.selectbox("Periodo", ["Último año", "Último trimestre", "Último mes", "Personalizado"])
        
        with col2:
            if periodo == "Personalizado":
                fecha_inicio, fecha_fin = st.date_input("Rango de fechas", [datetime.now() - timedelta(days=90), datetime.now()])
        
        # Generar datos según el periodo seleccionado
        if periodo == "Último año":
            meses, ingresos, gastos = generar_datos_mensuales(12)
        elif periodo == "Último trimestre":
            meses, ingresos, gastos = generar_datos_mensuales(3)
        elif periodo == "Último mes":
            meses, ingresos, gastos = generar_datos_mensuales(1)
        else:
            # Personalizado - usamos 12 meses por defecto
            meses, ingresos, gastos = generar_datos_mensuales(12)
            
        # Crear gráficos más detallados para el flujo de caja
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras para ingresos vs gastos
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=meses,
                y=ingresos,
                name='Ingresos',
                marker_color='#1E88E5',
                text=[f"{x:.2f} €" for x in ingresos],
                textposition='auto',
            ))
            
            fig.add_trace(go.Bar(
                x=meses,
                y=gastos,
                name='Gastos',
                marker_color='#FF5252',
                text=[f"{x:.2f} €" for x in gastos],
                textposition='auto',
            ))
            
            fig.update_layout(
                title='Comparación Ingresos vs Gastos',
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Gráfico de línea para el balance acumulado
            balance = [ingresos[i] - gastos[i] for i in range(len(ingresos))]
            balance_acumulado = np.cumsum(balance)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=balance_acumulado,
                mode='lines+markers',
                name='Balance Acumulado',
                line=dict(color='#4CAF50', width=3),
                fill='tozeroy',
                fillcolor='rgba(76, 175, 80, 0.2)'
            ))
            
            fig.update_layout(
                title='Balance Acumulado',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Indicadores de rentabilidad
        st.markdown("<h2 class='sub-header'>Indicadores Financieros</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_ingresos = sum(ingresos)
        total_gastos = sum(gastos)
        beneficio = total_ingresos - total_gastos
        margen = (beneficio / total_ingresos) * 100 if total_ingresos > 0 else 0
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Margen de Beneficio</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-value'>{margen:.1f}%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>ROI Mensual</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>18.3%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Periodo Medio de Cobro</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>32 días</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Liquidez</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>1.5x</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<h2 class='sub-header'>Análisis Predictivo</h2>", unsafe_allow_html=True)
        
        # Mensaje sobre la IA
        st.info("📊 **Análisis impulsado por IA**: Nuestros modelos predictivos analizan sus datos históricos para generar proyecciones financieras y recomendaciones.")
        
        # Proyección para los próximos meses
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Proyección de ingresos y gastos
            meses_hist, ingresos_hist, gastos_hist = generar_datos_mensuales(6, 0.03)
            
            # Agregar 3 meses de proyección con un poco más de variabilidad
            meses_proj = ["Ene", "Feb", "Mar"]
            
            ultimo_ingreso = ingresos_hist[-1]
            ultimo_gasto = gastos_hist[-1]
            
            ingresos_proj = [
                ultimo_ingreso * (1 + 0.05 + random.uniform(-0.02, 0.08)),
                ultimo_ingreso * (1 + 0.07 + random.uniform(-0.02, 0.09)),
                ultimo_ingreso * (1 + 0.09 + random.uniform(-0.03, 0.1))
            ]
            
            gastos_proj = [
                ultimo_gasto * (1 + 0.03 + random.uniform(-0.01, 0.04)),
                ultimo_gasto * (1 + 0.04 + random.uniform(-0.01, 0.05)),
                ultimo_gasto * (1 + 0.05 + random.uniform(-0.02, 0.06))
            ]
            
            # Combinar datos históricos y proyecciones
            meses_todos = meses_hist + meses_proj
            
            fig = go.Figure()
            
            # Datos históricos
            fig.add_trace(go.Scatter(
                x=meses_hist,
                y=ingresos_hist,
                mode='lines+markers',
                name='Ingresos (Histórico)',
                line=dict(color='#1E88E5', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=meses_hist,
                y=gastos_hist,
                mode='lines+markers',
                name='Gastos (Histórico)',
                line=dict(color='#FF5252', width=2)
            ))
            
            # Proyecciones
            fig.add_trace(go.Scatter(
                x=meses_proj,
                y=ingresos_proj,
                mode='lines+markers',
                name='Ingresos (Proyección)',
                line=dict(color='#1E88E5', width=2, dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=meses_proj,
                y=gastos_proj,
                mode='lines+markers',
                name='Gastos (Proyección)',
                line=dict(color='#FF5252', width=2, dash='dash')
            ))
            
            # Área sombreada para las proyecciones
            fig.add_vrect(
                x0=meses_hist[-1], x1=meses_proj[-1],
                fillcolor="rgba(200, 200, 200, 0.2)", opacity=0.7,
                layer="below", line_width=0,
            )
            
            fig.update_layout(
                title='Proyección Financiera para los Próximos 3 Meses',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=400,
                annotations=[
                    dict(
                        x=meses_proj[0],
                        y=max(ingresos_hist + ingresos_proj) * 1.1,
                        text="Proyección",
                        showarrow=False,
                        font=dict(size=14)
                    )
                ]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0;'>Recomendaciones de la IA</h3>", unsafe_allow_html=True)
            
            st.markdown("""
            <ul>
                <li><strong>Optimización de flujo de caja:</strong> Basado en su historial, recomendamos negociar términos de pago más favorables con los proveedores A y B.</li>
                <li><strong>Reducción de gastos:</strong> Detectamos un aumento del 15% en gastos de marketing sin un incremento proporcional en ingresos.</li>
                <li><strong>Oportunidad:</strong> Sus datos indican un ciclo estacional favorable en el próximo trimestre.</li>
            </ul>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3>Alertas</h3>", unsafe_allow_html=True)
            
            st.warning("📊 **Flujo de caja:** Proyectamos una posible disminución de liquidez en febrero si no se cobran las facturas pendientes.")
            st.success("✅ **Impuestos:** Todos los pagos fiscales están al día. Próximo vencimiento: 20/12/2023")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Previsión de tesorería
        st.markdown("<h2 class='sub-header'>Previsión de Tesorería</h2>", unsafe_allow_html=True)
        
        # Creamos datos simulados para la previsión
        dias = 90
        fechas_prev = [datetime.now() + timedelta(days=i) for i in range(dias)]
        fechas_str = [fecha.strftime("%d-%m") for fecha in fechas_prev]
        
        # Simulamos algunos pagos recurrentes
        saldo_inicial = 15243.00
        flujos = []
        
        for i in range(dias):
            flujo = 0
            
            # Ingresos mensuales (día 5 y 20)
            if fechas_prev[i].day == 5:
                flujo += random.uniform(3500, 4500)
            if fechas_prev[i].day == 20:
                flujo += random.uniform(3800, 4800)
                
            # Gastos fijos (alquiler día 1, nóminas día 28, etc.)
            if fechas_prev[i].day == 1:
                flujo -= 2000  # Alquiler
            if fechas_prev[i].day == 28:
                flujo -= 7000  # Nóminas
            if fechas_prev[i].day == 15:
                flujo -= 1500  # Suministros
                
            # Otros flujos aleatorios (facturas variables, etc.)
            if random.random() < 0.15:  # ~4-5 movimientos al mes
                if random.random() < 0.7:  # 70% gastos, 30% ingresos
                    flujo -= random.uniform(100, 1000)
                else:
                    flujo += random.uniform(200, 2000)
            
            flujos.append(flujo)
        
        # Calculamos el saldo acumulado
        saldo_acumulado = [saldo_inicial]
        for flujo in flujos:
            saldo_acumulado.append(saldo_acumulado[-1] + flujo)
        saldo_acumulado = saldo_acumulado[1:]  # Eliminamos el saldo inicial duplicado
        
        # Visualización de la previsión
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=fechas_str,
            y=saldo_acumulado,
            mode='lines',
            name='Saldo Previsto',
            line=dict(color='#4CAF50', width=2),
        ))
        
        # Línea de saldo mínimo recomendado
        saldo_minimo = 5000
        fig.add_trace(go.Scatter(
            x=[fechas_str[0], fechas_str[-1]],
            y=[saldo_minimo, saldo_minimo],
            mode='lines',
            name='Saldo Mínimo Recomendado',
            line=dict(color='#F44336', width=2, dash='dash'),
        ))
        
        # Formatear gráfico
        fig.update_layout(
            title='Previsión de Tesorería para los Próximos 90 Días',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                tickmode='array',
                tickvals=[fechas_str[i] for i in range(0, dias, 10)],
            ),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
            height=400,
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Información adicional sobre la previsión
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0;'>Análisis de Tesorería</h3>", unsafe_allow_html=True)
            
            # Calculamos algunos indicadores
            saldo_minimo_previsto = min(saldo_acumulado)
            fecha_saldo_minimo = fechas_prev[saldo_acumulado.index(saldo_minimo_previsto)].strftime("%d/%m/%Y")
            dias_bajo_minimo = sum(1 for saldo in saldo_acumulado if saldo < saldo_minimo)
            
            st.markdown(f"""
            <ul>
                <li><strong>Saldo mínimo previsto:</strong> {saldo_minimo_previsto:.2f} € (fecha: {fecha_saldo_minimo})</li>
                <li><strong>Días bajo el saldo mínimo recomendado:</strong> {dias_bajo_minimo}</li>
                <li><strong>Saldo final previsto:</strong> {saldo_acumulado[-1]:.2f} €</li>
                <li><strong>Variación prevista:</strong> {(saldo_acumulado[-1] - saldo_inicial):.2f} €</li>
            </ul>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top:0;'>Próximos Pagos Importantes</h3>", unsafe_allow_html=True)
            
            # Pagos importantes simulados
            st.markdown("""
            <table style="width:100%">
                <tr>
                    <th>Concepto</th>
                    <th>Fecha</th>
                    <th>Importe</th>
                </tr>
                <tr>
                    <td>Nóminas</td>
                    <td>28/11/2023</td>
                    <td>7.000,00 €</td>
                </tr>
                <tr>
                    <td>Alquiler</td>
                    <td>01/12/2023</td>
                    <td>2.000,00 €</td>
                </tr>
                <tr>
                    <td>Impuesto IVA</td>
                    <td>20/12/2023</td>
                    <td>2.154,33 €</td>
                </tr>
                <tr>
                    <td>Suministros</td>
                    <td>15/12/2023</td>
                    <td>1.500,00 €</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

elif opciones == "Transacciones":
    st.markdown("<h1 class='main-header'>Gestión de Transacciones</h1>", unsafe_allow_html=True)
    
    # Tabs para diferentes secciones
    tab1, tab2 = st.tabs(["📝 Registro de Transacciones", "🔍 Buscar y Filtrar"])
    
    with tab1:
        # Formulario para nueva transacción
        st.markdown("<h2 class='sub-header'>Nueva Transacción</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_trans = st.selectbox("Tipo de Transacción", ["Ingreso", "Gasto"])
            fecha_trans = st.date_input("Fecha", datetime.now())
            monto_trans = st.number_input("Monto (€)", min_value=0.01, step=10.0, value=100.0)
            
        with col2:
            if tipo_trans == "Ingreso":
                categoria_trans = st.selectbox("Categoría", ["Ventas", "Prestación de servicios", "Subvenciones", "Intereses", "Otros ingresos"])
            else:
                categoria_trans = st.selectbox("Categoría", ["Suministros", "Alquiler", "Salarios", "Marketing", "Software", "Equipamiento", "Seguros", "Impuestos", "Otros"])
            
            descripcion_trans = st.text_area("Descripción", height=100)
            cuenta_trans = st.selectbox("Cuenta", ["Cuenta Principal", "Cuenta Secundaria", "Efectivo", "Tarjeta de Crédito"])
        
        st.markdown("<div style='display: flex; justify-content: center; margin-top: 20px;'>", unsafe_allow_html=True)
        if st.button("Registrar Transacción", use_container_width=True):
            st.success(f"Transacción de {tipo_trans} por {monto_trans:.2f}€ registrada correctamente.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Últimas transacciones
        st.markdown("<h2 class='sub-header'>Últimas Transacciones</h2>", unsafe_allow_html=True)
        
        transacciones = generar_transacciones(20)
        transacciones = transacciones.sort_values(by='fecha', ascending=False)
        
        # Formatear fechas y montos para visualización
        transacciones['fecha_str'] = transacciones['fecha'].dt.strftime('%d/%m/%Y')
        transacciones['monto_str'] = transacciones['monto'].apply(lambda x: f"{x:.2f} €")
        
        # Aplicar estilo según el tipo (ingreso/gasto)
        def color_monto(val):
            tipo = val.split(' - ')[0]
            if tipo == 'Ingreso':
                return 'color: green'
            else:
                return 'color: red'
        
        # Mostrar tabla de transacciones
        st.dataframe(
            transacciones[['fecha_str', 'descripcion', 'monto_str']].rename(
                columns={'fecha_str': 'Fecha', 'descripcion': 'Descripción', 'monto_str': 'Monto'}
            ).style.applymap(color_monto, subset=['Descripción']),
            use_container_width=True,
            height=400
        )
    
    with tab2:
        st.markdown("<h2 class='sub-header'>Buscar y Filtrar Transacciones</h2>", unsafe_allow_html=True)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_tipo = st.multiselect("Tipo", ["Ingreso", "Gasto"], default=["Ingreso", "Gasto"])
        
        with col2:
            categorias = ["Ventas", "Prestación de servicios", "Subvenciones", "Intereses", "Otros ingresos", 
                         "Suministros", "Alquiler", "Salarios", "Marketing", "Software", "Equipamiento", "Seguros", "Impuestos", "Otros"]
            filtro_categoria = st.multiselect("Categoría", categorias)
        
        with col3:
            fecha_inicio, fecha_fin = st.date_input("Rango de fechas", [datetime.now() - timedelta(days=30), datetime.now()])
        
        # Filtro por texto
        filtro_texto = st.text_input("Buscar por descripción")
        
        # Generar transacciones filtradas (simulado)
        todas_transacciones = generar_transacciones(100)
        
        # Aplicar filtros
        transacciones_filtradas = todas_transacciones.copy()
        
        if filtro_tipo:
            transacciones_filtradas = transacciones_filtradas[transacciones_filtradas['tipo'].isin(filtro_tipo)]
        
        if filtro_categoria:
            transacciones_filtradas = transacciones_filtradas[transacciones_filtradas['categoria'].isin(filtro_categoria)]

        if filtro_texto:
            transacciones_filtradas = transacciones_filtradas[transacciones_filtradas['descripcion'].str.contains(filtro_texto, case=False)]
        
        # Formatear para mostrar
        transacciones_filtradas['fecha_str'] = transacciones_filtradas['fecha'].dt.strftime('%d/%m/%Y')
        transacciones_filtradas['monto_str'] = transacciones_filtradas['monto'].apply(lambda x: f"{x:.2f} €")
        
        # Mostrar resultados
        st.markdown(f"<h3>Resultados: {len(transacciones_filtradas)} transacciones encontradas</h3>", unsafe_allow_html=True)
        
        # Mostrar tabla de transacciones
        st.dataframe(
            transacciones_filtradas[['fecha_str', 'descripcion', 'categoria', 'monto_str']].rename(
                columns={'fecha_str': 'Fecha', 'descripcion': 'Descripción', 'categoria': 'Categoría', 'monto_str': 'Monto'}
            ),
            use_container_width=True,
            height=400
        )
        
        # Exportar resultados
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Exportar a Excel", use_container_width=True):
                st.success("Datos exportados correctamente.")
                
        with col2:
            if st.button("Generar Informe PDF", use_container_width=True):
                st.success("Informe PDF generado correctamente.")
        
        # Visualización de transacciones filtradas
        if not transacciones_filtradas.empty:
            st.markdown("<h3>Análisis de Transacciones Filtradas</h3>", unsafe_allow_html=True)
            
            # Gráfico según categorías
            categorias_counts = transacciones_filtradas['categoria'].value_counts()
            
            fig = px.pie(
                names=categorias_counts.index,
                values=categorias_counts.values,
                title='Distribución por Categorías',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)

elif opciones == "Facturas":
    st.markdown("<h1 class='main-header'>Gestión de Facturas</h1>", unsafe_allow_html=True)
    
    # Tabs para diferentes secciones
    tab1, tab2, tab3 = st.tabs(["📋 Listado de Facturas", "➕ Nueva Factura", "📊 Análisis de Cobros"])
    
    with tab1:
        # Listado de facturas con filtros
        st.markdown("<h2 class='sub-header'>Listado de Facturas</h2>", unsafe_allow_html=True)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_estado = st.multiselect("Estado", ["Pendiente", "Pagada", "Vencida"], default=["Pendiente", "Vencida"])
        
        with col2:
            fecha_inicio, fecha_fin = st.date_input("Rango de emisión", [datetime.now() - timedelta(days=90), datetime.now()])
        
        with col3:
            filtro_cliente = st.text_input("Cliente")
        
        # Generar facturas
        facturas = generar_facturas(30)
        
        # Aplicar filtros (simulado)
        facturas_filtradas = facturas.copy()
        
        if filtro_estado:
            facturas_filtradas = facturas_filtradas[facturas_filtradas['estado'].isin(filtro_estado)]
        
        if filtro_cliente:
            facturas_filtradas = facturas_filtradas[facturas_filtradas['cliente'].str.contains(filtro_cliente, case=False)]
        
        # Formatear fechas y montos para visualización
        facturas_filtradas['fecha_emision_str'] = facturas_filtradas['fecha_emision'].dt.strftime('%d/%m/%Y')
        facturas_filtradas['vencimiento_str'] = facturas_filtradas['vencimiento'].dt.strftime('%d/%m/%Y')
        facturas_filtradas['monto_str'] = facturas_filtradas['monto'].apply(lambda x: f"{x:.2f} €")
        
        # Colorear según estado
        def colorear_estado(val):
            if val == 'Pendiente':
                return 'background-color: #FFF9C4'
            elif val == 'Pagada':
                return 'background-color: #C8E6C9'
            else:  # Vencida
                return 'background-color: #FFCDD2'
        
        # Mostrar tabla de facturas
        st.dataframe(
            facturas_filtradas[['numero', 'cliente', 'fecha_emision_str', 'vencimiento_str', 'monto_str', 'estado']].rename(
                columns={
                    'numero': 'Número', 
                    'cliente': 'Cliente', 
                    'fecha_emision_str': 'Emisión', 
                    'vencimiento_str': 'Vencimiento',
                    'monto_str': 'Importe',
                    'estado': 'Estado'
                }
            ).style.applymap(colorear_estado, subset=['Estado']),
            use_container_width=True,
            height=400
        )
        
        # Acciones de facturas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Marcar como Pagada", use_container_width=True):
                st.success("Estado de factura actualizado correctamente.")
                
        with col2:
            if st.button("Enviar Recordatorio", use_container_width=True):
                st.success("Recordatorio enviado correctamente.")
                
        with col3:
            if st.button("Exportar Facturas", use_container_width=True):
                st.success("Facturas exportadas correctamente.")
    
    with tab2:
        # Formulario para nueva factura
        st.markdown("<h2 class='sub-header'>Crear Nueva Factura</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            cliente = st.text_input("Cliente", key="factura_nuevo_cliente")
            fecha_emision = st.date_input("Fecha de Emisión", datetime.now(), key="factura_fecha_emision")
            dias_vencimiento = st.number_input("Días para Vencimiento", min_value=0, value=30, key="factura_dias_vencimiento")
            fecha_vencimiento = fecha_emision + timedelta(days=dias_vencimiento)
            st.info(f"Fecha de vencimiento: {fecha_vencimiento.strftime('%d/%m/%Y')}")
            
        with col2:
            nif_cliente = st.text_input("NIF/CIF Cliente", key="factura_nif_cliente")
            direccion = st.text_area("Dirección de Facturación", height=100, key="factura_direccion")
            forma_pago = st.selectbox("Forma de Pago", ["Transferencia Bancaria", "Domiciliación", "Efectivo", "Tarjeta", "PayPal"], key="factura_forma_pago")
        
        # Tabla para añadir conceptos
        st.markdown("<h3>Conceptos</h3>", unsafe_allow_html=True)
        
        # Inicializar estado de la sesión para los conceptos si no existe
        if 'conceptos' not in st.session_state:
            st.session_state.conceptos = []
            st.session_state.contador_conceptos = 0
        
        # Formulario para añadir concepto
        with st.expander("Añadir Concepto", expanded=True):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                concepto_desc = st.text_input("Descripción")
            
            with col2:
                concepto_cant = st.number_input("Cantidad", min_value=1, value=1)
            
            with col3:
                concepto_precio = st.number_input("Precio Unitario (€)", min_value=0.01, value=100.00)
            
            with col4:
                concepto_iva = st.selectbox("IVA (%)", [0, 4, 10, 21], index=3)
            
            if st.button("Añadir Concepto"):
                subtotal = concepto_cant * concepto_precio
                iva = subtotal * (concepto_iva / 100)
                total = subtotal + iva
                
                st.session_state.conceptos.append({
                    'id': st.session_state.contador_conceptos,
                    'descripcion': concepto_desc,
                    'cantidad': concepto_cant,
                    'precio': concepto_precio,
                    'iva_porcentaje': concepto_iva,
                    'subtotal': subtotal,
                    'iva': iva,
                    'total': total
                })
                
                st.session_state.contador_conceptos += 1
        
        # Mostrar conceptos añadidos
        if st.session_state.conceptos:
            conceptos_df = pd.DataFrame(st.session_state.conceptos)
            
            # Formatear para mostrar
            conceptos_df['precio_str'] = conceptos_df['precio'].apply(lambda x: f"{x:.2f} €")
            conceptos_df['subtotal_str'] = conceptos_df['subtotal'].apply(lambda x: f"{x:.2f} €")
            conceptos_df['iva_str'] = conceptos_df['iva'].apply(lambda x: f"{x:.2f} €")
            conceptos_df['total_str'] = conceptos_df['total'].apply(lambda x: f"{x:.2f} €")
            
            st.dataframe(
                conceptos_df[['descripcion', 'cantidad', 'precio_str', 'iva_porcentaje', 'subtotal_str', 'iva_str', 'total_str']].rename(
                    columns={
                        'descripcion': 'Descripción',
                        'cantidad': 'Cantidad',
                        'precio_str': 'Precio Unit.',
                        'iva_porcentaje': 'IVA %',
                        'subtotal_str': 'Subtotal',
                        'iva_str': 'IVA',
                        'total_str': 'Total'
                    }
                ),
                use_container_width=True,
                height=200
            )
            
            # Mostrar totales
            total_sin_iva = conceptos_df['subtotal'].sum()
            total_iva = conceptos_df['iva'].sum()
            total_factura = conceptos_df['total'].sum()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-label'>Base Imponible</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{total_sin_iva:.2f} €</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-label'>IVA</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{total_iva:.2f} €</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-label'>Total Factura</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-value'>{total_factura:.2f} €</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Botones para acciones de factura
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Limpiar Conceptos", use_container_width=True):
                    st.session_state.conceptos = []
                    st.experimental_rerun()
            
            with col2:
                if st.button("Guardar Factura", use_container_width=True):
                    st.success(f"Factura para {cliente} por {total_factura:.2f}€ creada correctamente.")
                    # Aquí iría el código para guardar la factura en la base de datos
        
        # Si no hay conceptos, mostrar mensaje
        else:
            st.info("Añade conceptos a la factura usando el formulario de arriba.")
    
    with tab3:
        # Análisis de cobros y pagos
        st.markdown("<h2 class='sub-header'>Análisis de Cobros</h2>", unsafe_allow_html=True)
        
        # Generar datos simulados para el análisis
        facturas = generar_facturas(50)
        
        # Calcular estadísticas
        pendientes = facturas[facturas['estado'] == 'Pendiente']
        pagadas = facturas[facturas['estado'] == 'Pagada']
        vencidas = facturas[facturas['estado'] == 'Vencida']
        
        total_pendiente = pendientes['monto'].sum()
        total_pagado = pagadas['monto'].sum()
        total_vencido = vencidas['monto'].sum()
        
        # Mostrar métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Pendiente de Cobro</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-value'>{total_pendiente:.2f} €</p>", unsafe_allow_html=True)
            st.markdown(f"<p>({len(pendientes)} facturas)</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Cobrado</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-value'>{total_pagado:.2f} €</p>", unsafe_allow_html=True)
            st.markdown(f"<p>({len(pagadas)} facturas)</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Vencido</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-value'>{total_vencido:.2f} €</p>", unsafe_allow_html=True)
            st.markdown(f"<p>({len(vencidas)} facturas)</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Gráfico de estado de facturas
        estados_count = facturas['estado'].value_counts()
        
        fig = px.pie(
            names=estados_count.index,
            values=estados_count.values,
            title='Distribución de Facturas por Estado',
            color_discrete_map={
                'Pendiente': '#FFC107',
                'Pagada': '#4CAF50',
                'Vencida': '#F44336'
            },
            hole=0.4
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Periodo medio de cobro
        st.markdown("<h3>Periodo Medio de Cobro</h3>", unsafe_allow_html=True)
        
        # Simular datos de periodo de cobro
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        dias_cobro = [32, 35, 30, 28, 33, 29, 27, 34, 31, 30, 29, 28]
        
        fig = px.bar(
            x=meses,
            y=dias_cobro,
            title="Periodo Medio de Cobro por Mes (días)",
            labels={'x': 'Mes', 'y': 'Días'},
            color_discrete_sequence=['#1E88E5']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
            height=400,
            yaxis_range=[0, max(dias_cobro) * 1.2]
        )
        
        fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Objetivo (30 días)")
        
        st.plotly_chart(fig, use_container_width=True)

elif opciones == "Informes":
    st.markdown("<h1 class='main-header'>Informes Financieros</h1>", unsafe_allow_html=True)
    
    # Tabs para diferentes tipos de informes
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumen", "💰 Cuenta de Resultados", "📈 Balance", "💼 Impuestos"])
    
    with tab1:
        # Informe de resumen
        st.markdown("<h2 class='sub-header'>Resumen Financiero</h2>", unsafe_allow_html=True)
        
        # Selector de periodo
        col1, col2 = st.columns([1, 2])
        with col1:
            periodo = st.selectbox("Periodo", ["Mensual", "Trimestral", "Anual", "Personalizado"], key="resumen_periodo")
        
        with col2:
            if periodo == "Personalizado":
                fecha_inicio, fecha_fin = st.date_input("Rango de fechas", [datetime.now() - timedelta(days=90), datetime.now()], key="resumen_fechas")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Ingresos</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>85.432,18 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-positive'>↑ 12.5% vs. periodo anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Gastos</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>65.987,42 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-negative'>↑ 8.2% vs. periodo anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Beneficio</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>19.444,76 €</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-positive'>↑ 28.7% vs. periodo anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Margen</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>22.8%</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-delta-positive'>↑ 3.5 puntos vs. periodo anterior</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Gráfica de evolución
        st.markdown("<h3>Evolución Financiera</h3>", unsafe_allow_html=True)
        
        # Datos simulados
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        ingresos = [15000, 16200, 15800, 17000, 16500, 18000, 19500, 18000, 20000, 21500, 19800, 22000]
        gastos = [12000, 12500, 13000, 13200, 13500, 14000, 15000, 14500, 15500, 16000, 15800, 17000]
        beneficios = [ingresos[i] - gastos[i] for i in range(len(ingresos))]
        
        # Crear dataframe para gráfico
        df_evolucion = pd.DataFrame({
            'Mes': meses * 3,
            'Tipo': ['Ingresos'] * 12 + ['Gastos'] * 12 + ['Beneficio'] * 12,
            'Valor': ingresos + gastos + beneficios
        })
        
        fig = px.line(
            df_evolucion, 
            x='Mes', 
            y='Valor', 
            color='Tipo',
            color_discrete_map={
                'Ingresos': '#4CAF50', 
                'Gastos': '#FF5252', 
                'Beneficio': '#2196F3'
            },
            markers=True,
            title='Evolución Financiera Anual'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribución de gastos e ingresos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>Distribución de Ingresos</h3>", unsafe_allow_html=True)
            
            # Datos simulados
            categorias_ingresos = ["Ventas de productos", "Servicios recurrentes", "Servicios puntuales", "Otros ingresos"]
            valores_ingresos = [50000, 25000, 8000, 2432.18]
            
            fig = px.pie(
                names=categorias_ingresos,
                values=valores_ingresos,
                title='Ingresos por Categoría',
                color_discrete_sequence=px.colors.qualitative.G10,
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("<h3>Distribución de Gastos</h3>", unsafe_allow_html=True)
            
            # Datos simulados
            categorias_gastos, valores_gastos = generar_categorias_gastos()
            
            fig = px.pie(
                names=categorias_gastos,
                values=valores_gastos,
                title='Gastos por Categoría',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Botones para exportar
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("Exportar a Excel", use_container_width=True):
                st.success("Informe exportado a Excel correctamente.")
                
        with col2:
            if st.button("Generar PDF", use_container_width=True):
                st.success("Informe PDF generado correctamente.")
    
    with tab2:
        st.markdown("<h2 class='sub-header'>Cuenta de Resultados</h2>", unsafe_allow_html=True)
        
        # Selector de periodo
        col1, col2 = st.columns([1, 2])
        with col1:
            periodo_cr = st.selectbox("Periodo", ["Mensual", "Trimestral", "Anual", "Personalizado"], key="cr_periodo")
        
        with col2:
            if periodo_cr == "Personalizado":
                fecha_inicio_cr, fecha_fin_cr = st.date_input("Rango de fechas", [datetime.now() - timedelta(days=90), datetime.now()], key="cr_fechas")
        
        # Tabla de cuenta de resultados
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Datos simulados de cuenta de resultados
        cuenta_resultados = [
            {"concepto": "1. Importe neto de la cifra de negocios", "valor": 85432.18, "porcentaje": 100.0},
            {"concepto": "4. Aprovisionamientos", "valor": -12543.21, "porcentaje": -14.7},
            {"concepto": "5. Otros ingresos de explotación", "valor": 2150.00, "porcentaje": 2.5},
            {"concepto": "6. Gastos de personal", "valor": -35000.00, "porcentaje": -41.0},
            {"concepto": "7. Otros gastos de explotación", "valor": -15231.42, "porcentaje": -17.8},
            {"concepto": "8. Amortización del inmovilizado", "valor": -3212.79, "porcentaje": -3.8},
            {"concepto": "A) RESULTADO DE EXPLOTACIÓN", "valor": 21594.76, "porcentaje": 25.3},
            {"concepto": "12. Ingresos financieros", "valor": 150.00, "porcentaje": 0.2},
            {"concepto": "13. Gastos financieros", "valor": -2300.00, "porcentaje": -2.7},
            {"concepto": "B) RESULTADO FINANCIERO", "valor": -2150.00, "porcentaje": -2.5},
            {"concepto": "C) RESULTADO ANTES DE IMPUESTOS", "valor": 19444.76, "porcentaje": 22.8},
            {"concepto": "17. Impuestos sobre beneficios", "valor": -4861.19, "porcentaje": -5.7},
            {"concepto": "D) RESULTADO DEL EJERCICIO", "valor": 14583.57, "porcentaje": 17.1}
        ]
        
        # Convertir a DataFrame
        df_cr = pd.DataFrame(cuenta_resultados)
        
        # Formatear para mostrar
        df_cr['valor_str'] = df_cr['valor'].apply(lambda x: f"{x:,.2f} €".replace(',', '.'))
        df_cr['porcentaje_str'] = df_cr['porcentaje'].apply(lambda x: f"{x:.1f}%")
        
        # Estilos personalizados para filas específicas
        def estilo_fila(row):
            if 'concepto' in row.index:  # Verifica si la columna existe
                if row.get('concepto', '').startswith(('A)', 'B)', 'C)', 'D)')):
                return ['background-color: #E3F2FD; font-weight: bold;'] * len(row)
            return [''] * len(row)
        
        # Mostrar tabla
        st.markdown("<h3>Cuenta de Resultados</h3>", unsafe_allow_html=True)
        
        if 'concepto' in df_cr.columns:
            styled_df = df_cr[['concepto', 'valor_str', 'porcentaje_str']].rename(
                columns={
                    'concepto': 'Concepto',
                    'valor_str': 'Valor',
                    'porcentaje_str': '% sobre ventas'
                }
            ).style.apply(estilo_fila, axis=1)
        else:
            # Usa un enfoque alternativo si 'concepto' no está en el DataFrame
            styled_df = df_cr.rename(
                columns={
                    'concepto': 'Concepto',
                    'valor_str': 'Valor',
                    'porcentaje_str': '% sobre ventas'
                }
            )

        st.dataframe(styled_df, use_container_width=True, height=500)
        
        # Gráfico de comparación con periodo anterior
        st.markdown("<h3>Comparativa con Periodo Anterior</h3>", unsafe_allow_html=True)
        
        # Datos simulados
        conceptos_comp = ["Ventas", "Gastos Personal", "Otros Gastos", "Resultado"]
        valores_actual = [85432.18, 35000.00, 31000.00, 14583.57]
        valores_anterior = [75800.00, 32500.00, 28900.00, 11300.00]
        
        # Crear dataframe para gráfico
        df_comp = pd.DataFrame({
            'Concepto': conceptos_comp * 2,
            'Periodo': ['Actual'] * 4 + ['Anterior'] * 4,
            'Valor': valores_actual + valores_anterior
        })
        
        fig = px.bar(
            df_comp,
            x='Concepto',
            y='Valor',
            color='Periodo',
            barmode='group',
            color_discrete_map={
                'Actual': '#1E88E5',
                'Anterior': '#90CAF9'
            },
            title='Comparativa con Periodo Anterior'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab3:
        st.markdown("<h2 class='sub-header'>Balance de Situación</h2>", unsafe_allow_html=True)
        
        # Fecha de balance
        fecha_balance = st.date_input("Fecha del Balance", datetime.now())
        
        # Dividir en activo y pasivo
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>Activo</h3>", unsafe_allow_html=True)
            
            # Datos simulados del activo
            activo = [
                {"concepto": "A) ACTIVO NO CORRIENTE", "valor": 45000.00},
                {"concepto": "I. Inmovilizado intangible", "valor": 8000.00},
                {"concepto": "II. Inmovilizado material", "valor": 32000.00},
                {"concepto": "V. Inversiones financieras a largo plazo", "valor": 5000.00},
                {"concepto": "B) ACTIVO CORRIENTE", "valor": 63500.00},
                {"concepto": "II. Existencias", "valor": 12000.00},
                {"concepto": "III. Deudores comerciales y otras cuentas a cobrar", "valor": 28500.00},
                {"concepto": "VII. Efectivo y otros activos líquidos equivalentes", "valor": 23000.00},
                {"concepto": "TOTAL ACTIVO (A+B)", "valor": 108500.00}
            ]
            
            # Convertir a DataFrame
            df_activo = pd.DataFrame(activo)
            
            # Formatear para mostrar
            df_activo['valor_str'] = df_activo['valor'].apply(lambda x: f"{x:,.2f} €".replace(',', '.'))
            
            # Estilos personalizados para filas específicas
            def estilo_fila_balance(row):
                if row['concepto'].startswith('A)') or row['concepto'].startswith('B)') or row['concepto'].startswith('TOTAL'):
                    return ['background-color: #E3F2FD; font-weight: bold;'] * len(row)
                return [''] * len(row)
            
            # Mostrar tabla
            st.dataframe(
                df_activo[['concepto', 'valor_str']].rename(
                    columns={
                        'concepto': 'Concepto',
                        'valor_str': 'Valor'
                    }
                ).style.apply(estilo_fila_balance, axis=1),
                use_container_width=True,
                height=300
            )
        
        with col2:
            st.markdown("<h3>Patrimonio Neto y Pasivo</h3>", unsafe_allow_html=True)
            
            # Datos simulados del pasivo
            pasivo = [
                {"concepto": "A) PATRIMONIO NETO", "valor": 65000.00},
                {"concepto": "I. Capital", "valor": 20000.00},
                {"concepto": "III. Reservas", "valor": 30416.43},
                {"concepto": "VII. Resultado del ejercicio", "valor": 14583.57},
                {"concepto": "B) PASIVO NO CORRIENTE", "valor": 15000.00},
                {"concepto": "II. Deudas a largo plazo", "valor": 15000.00},
                {"concepto": "C) PASIVO CORRIENTE", "valor": 28500.00},
                {"concepto": "III. Deudas a corto plazo", "valor": 5000.00},
                {"concepto": "V. Acreedores comerciales y otras cuentas a pagar", "valor": 23500.00},
                {"concepto": "TOTAL PATRIMONIO NETO Y PASIVO (A+B+C)", "valor": 108500.00}
            ]
            
            # Convertir a DataFrame
            df_pasivo = pd.DataFrame(pasivo)
            
            # Formatear para mostrar
            df_pasivo['valor_str'] = df_pasivo['valor'].apply(lambda x: f"{x:,.2f} €".replace(',', '.'))
            
            # Mostrar tabla
            st.dataframe(
                df_pasivo[['concepto', 'valor_str']].rename(
                    columns={
                        'concepto': 'Concepto',
                        'valor_str': 'Valor'
                    }
                ).style.apply(estilo_fila_balance, axis=1),
                use_container_width=True,
                height=350
            )
        
        # Gráficos de composición del balance
        st.markdown("<h3>Composición del Balance</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Composición del activo
            labels_activo = ["Activo No Corriente", "Activo Corriente"]
            valores_activo = [45000.00, 63500.00]
            
            fig = px.pie(
                names=labels_activo,
                values=valores_activo,
                title='Composición del Activo',
                color_discrete_sequence=['#1E88E5', '#42A5F5'],
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Composición del pasivo
            labels_pasivo = ["Patrimonio Neto", "Pasivo No Corriente", "Pasivo Corriente"]
            valores_pasivo = [65000.00, 15000.00, 28500.00]
            
            fig = px.pie(
                names=labels_pasivo,
                values=valores_pasivo,
                title='Composición del Patrimonio Neto y Pasivo',
                color_discrete_sequence=['#4CAF50', '#FFC107', '#FF5252'],
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Ratios financieros
        st.markdown("<h3>Ratios Financieros</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Ratio de Liquidez</p>", unsafe_allow_html=True)
            liquidez = 63500.00 / 28500.00
            st.markdown(f"<p class='metric-value'>{liquidez:.2f}</p>", unsafe_allow_html=True)
            st.markdown("<p>Óptimo > 1.5</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>Ratio de Endeudamiento</p>", unsafe_allow_html=True)
            endeudamiento = (15000.00 + 28500.00) / 108500.00 * 100
            st.markdown(f"<p class='metric-value'>{endeudamiento:.1f}%</p>", unsafe_allow_html=True)
            st.markdown("<p>Óptimo entre 40% y 60%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>ROE</p>", unsafe_allow_html=True)
            roe = 14583.57 / 65000.00 * 100
            st.markdown(f"<p class='metric-value'>{roe:.1f}%</p>", unsafe_allow_html=True)
            st.markdown("<p>Rentabilidad Financiera</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='metric-label'>ROA</p>", unsafe_allow_html=True)
            roa = 14583.57 / 108500.00 * 100
            st.markdown(f"<p class='metric-value'>{roa:.1f}%</p>", unsafe_allow_html=True)
            st.markdown("<p>Rentabilidad Económica</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<h2 class='sub-header'>Gestión de Impuestos</h2>", unsafe_allow_html=True)
        
        # Calendario fiscal
        st.markdown("<h3>Calendario Fiscal</h3>", unsafe_allow_html=True)
        
        # Obtener el año actual
        año_actual = datetime.now().year
        
        # Datos simulados del calendario fiscal
        calendario_fiscal = [
            {"impuesto": "IVA", "periodo": "Primer trimestre", "fecha_limite": f"20/04/{año_actual}", "estado": "Pagado", "importe": 3250.45},
            {"impuesto": "IVA", "periodo": "Segundo trimestre", "fecha_limite": f"20/07/{año_actual}", "estado": "Pagado", "importe": 3842.18},
            {"impuesto": "IVA", "periodo": "Tercer trimestre", "fecha_limite": f"20/10/{año_actual}", "estado": "Pagado", "importe": 4120.75},
            {"impuesto": "IVA", "periodo": "Cuarto trimestre", "fecha_limite": f"30/01/{año_actual+1}", "estado": "Pendiente", "importe": 2154.33},
            {"impuesto": "Impuesto de Sociedades", "periodo": "Anual", "fecha_limite": f"25/07/{año_actual}", "estado": "Pagado", "importe": 4861.19},
            {"impuesto": "Retenciones IRPF", "periodo": "Primer trimestre", "fecha_limite": f"20/04/{año_actual}", "estado": "Pagado", "importe": 1845.00},
            {"impuesto": "Retenciones IRPF", "periodo": "Segundo trimestre", "fecha_limite": f"20/07/{año_actual}", "estado": "Pagado", "importe": 1845.00},
            {"impuesto": "Retenciones IRPF", "periodo": "Tercer trimestre", "fecha_limite": f"20/10/{año_actual}", "estado": "Pagado", "importe": 1845.00},
            {"impuesto": "Retenciones IRPF", "periodo": "Cuarto trimestre", "fecha_limite": f"20/01/{año_actual+1}", "estado": "Pendiente", "importe": 1845.00}
        ]
        
        # Convertir a DataFrame
        df_calendario = pd.DataFrame(calendario_fiscal)
        
        # Formatear para mostrar
        df_calendario['importe_str'] = df_calendario['importe'].apply(lambda x: f"{x:,.2f} €".replace(',', '.'))
        
        # Colorear según estado
        def colorear_estado_impuesto(val):
            if val == 'Pagado':
                return 'background-color: #C8E6C9'
            elif val == 'Pendiente':
                return 'background-color: #FFF9C4'
            else:  # Vencido
                return 'background-color: #FFCDD2'
        
        # Mostrar tabla
        st.dataframe(
            df_calendario[['impuesto', 'periodo', 'fecha_limite', 'estado', 'importe_str']].rename(
                columns={
                    'impuesto': 'Impuesto',
                    'periodo': 'Periodo',
                    'fecha_limite': 'Fecha Límite',
                    'estado': 'Estado',
                    'importe_str': 'Importe'
                }
            ).style.applymap(colorear_estado_impuesto, subset=['Estado']),
            use_container_width=True,
            height=300
        )
        
        # Resumen de impuestos
        st.markdown("<h3>Resumen de Impuestos Anuales</h3>", unsafe_allow_html=True)
        
        # Totales por tipo de impuesto
        totales_impuestos = df_calendario.groupby('impuesto')['importe'].sum().reset_index()
        totales_impuestos['importe_str'] = totales_impuestos['importe'].apply(lambda x: f"{x:,.2f} €".replace(',', '.'))
        
        # Gráfico de barras
        fig = px.bar(
            totales_impuestos,
            x='impuesto',
            y='importe',
            title='Total de Impuestos por Tipo',
            color='impuesto',
            color_discrete_sequence=px.colors.qualitative.Safe,
            labels={'impuesto': 'Impuesto', 'importe': 'Importe Total'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.6)'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Simulador de impuestos
        st.markdown("<h3>Simulador de Impuestos</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Simulador de IVA
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>Simulador de IVA</h4>", unsafe_allow_html=True)
            
            base_imponible = st.number_input("Base Imponible (€)", min_value=0.0, value=10000.0, step=1000.0)
            tipo_iva = st.selectbox("Tipo de IVA", [4, 10, 21], index=2)
            
            cuota_iva = base_imponible * (tipo_iva / 100)
            total = base_imponible + cuota_iva
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<p><b>Cuota IVA:</b> {cuota_iva:.2f} €</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p><b>Total:</b> {total:.2f} €</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            # Simulador de IRPF
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>Simulador de Retenciones IRPF</h4>", unsafe_allow_html=True)
            
            base_retencion = st.number_input("Base de Retención (€)", min_value=0.0, value=5000.0, step=500.0)
            tipo_retencion = st.slider("Tipo de Retención (%)", min_value=0, max_value=50, value=15)
            
            retencion = base_retencion * (tipo_retencion / 100)
            liquido = base_retencion - retencion
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<p><b>Retención IRPF:</b> {retencion:.2f} €</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p><b>Líquido a percibir:</b> {liquido:.2f} €</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

elif opciones == "Configuración":
    st.markdown("<h1 class='main-header'>Configuración del Sistema</h1>", unsafe_allow_html=True)
    
    # Tabs para diferentes configuraciones
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ General", "👥 Usuarios", "🏢 Empresa", "📊 Exportación"])
    
    with tab1:
        st.markdown("<h2 class='sub-header'>Configuración General</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Preferencias</h3>", unsafe_allow_html=True)
            
            moneda = st.selectbox("Moneda", ["EUR (€)", "USD ($)", "GBP (£)"], index=0)
            decimales = st.selectbox("Decimales en importes", [0, 1, 2], index=2)
            fecha_formato = st.selectbox("Formato de fecha", ["DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"], index=0)
            tema = st.selectbox("Tema", ["Claro", "Oscuro", "Sistema"], index=0)
            
            st.markdown("<h3>Notificaciones</h3>", unsafe_allow_html=True)
            st.checkbox("Notificaciones por email", value=True)
            st.checkbox("Recordatorios de facturas pendientes", value=True)
            st.checkbox("Alertas de flujo de caja", value=True)
            st.checkbox("Notificaciones de vencimientos fiscales", value=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Integración con IA</h3>", unsafe_allow_html=True)
            
            st.checkbox("Categorización automática de gastos", value=True)
            st.checkbox("Predicción de flujo de caja", value=True)
            st.checkbox("Recomendaciones financieras", value=True)
            
            st.markdown("<h3>Ajustes de Predicciones</h3>", unsafe_allow_html=True)
            
            horizonte_prediccion = st.slider("Horizonte de predicción (días)", min_value=30, max_value=365, value=90, step=30)
            intervalo_confianza = st.slider("Intervalo de confianza (%)", min_value=70, max_value=99, value=95)
            
            st.markdown("<h3>Conexiones Externas</h3>", unsafe_allow_html=True)
            
            st.checkbox("Conectar con banco", value=False)
            st.checkbox("Sincronizar con software contable", value=False)
            st.checkbox("Integración con CRM", value=False)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Botón para guardar configuración
        if st.button("Guardar Configuración", use_container_width=True):
            st.success("Configuración guardada correctamente.")
    
    with tab2:
        st.markdown("<h2 class='sub-header'>Gestión de Usuarios</h2>", unsafe_allow_html=True)
        
        # Lista de usuarios simulada
        usuarios = [
            {"id": 1, "nombre": "Administrador Principal", "email": "admin@empresa.com", "rol": "Administrador", "estado": "Activo"},
            {"id": 2, "nombre": "Usuario Contabilidad", "email": "contabilidad@empresa.com", "rol": "Editor", "estado": "Activo"},
            {"id": 3, "nombre": "Usuario Ventas", "email": "ventas@empresa.com", "rol": "Visualizador", "estado": "Activo"},
            {"id": 4, "nombre": "Usuario Antiguo", "email": "antiguo@empresa.com", "rol": "Visualizador", "estado": "Inactivo"}
        ]
        
        # Convertir a DataFrame
        df_usuarios = pd.DataFrame(usuarios)
        
        # Mostrar tabla
        st.dataframe(
            df_usuarios[['nombre', 'email', 'rol', 'estado']].rename(
                columns={
                    'nombre': 'Nombre',
                    'email': 'Email',
                    'rol': 'Rol',
                    'estado': 'Estado'
                }
            ),
            use_container_width=True,
            height=200
        )
        
        # Formulario para nuevo usuario
        st.markdown("<h3>Añadir Nuevo Usuario</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nuevo_nombre = st.text_input("Nombre completo")
            nuevo_email = st.text_input("Email")
            
        with col2:
            nuevo_rol = st.selectbox("Rol", ["Administrador", "Editor", "Visualizador"])
            nuevo_password = st.text_input("Contraseña", type="password")
        
        if st.button("Añadir Usuario", use_container_width=True):
            st.success(f"Usuario {nuevo_nombre} añadido correctamente.")
    
    with tab3:
        st.markdown("<h2 class='sub-header'>Datos de la Empresa</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Información Básica</h3>", unsafe_allow_html=True)
            
            nombre_empresa = st.text_input("Nombre de la empresa", value="Empresa ACME, S.L.")
            cif = st.text_input("CIF/NIF", value="B12345678")
            direccion = st.text_area("Dirección fiscal", value="Calle Principal, 123\n28001 Madrid")
            telefono = st.text_input("Teléfono", value="+34 912 345 678")
            email = st.text_input("Email", value="info@empresa-acme.com")
            web = st.text_input("Página web", value="www.empresa-acme.com")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Información Fiscal y Bancaria</h3>", unsafe_allow_html=True)
            
            regimen_fiscal = st.selectbox("Régimen fiscal", ["General", "Módulos", "Agrario", "Simplificado"])
            actividad_economica = st.text_input("Actividad económica", value="Consultoría informática")
            codigo_cnae = st.text_input("Código CNAE", value="6201")
            
            st.markdown("<h4>Datos Bancarios</h4>", unsafe_allow_html=True)
            banco = st.text_input("Banco", value="Banco Ejemplo")
            iban = st.text_input("IBAN", value="ES12 3456 7890 1234 5678 9012")
            swift = st.text_input("SWIFT/BIC", value="EXAMPLEXXX")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Logo de la empresa
        st.markdown("<h3>Logo de la Empresa</h3>", unsafe_allow_html=True)
        
        # Simular carga de imagen
        logo_file = st.file_uploader("Subir logo (formato PNG o JPG)", type=["png", "jpg", "jpeg"])
        
        # Mostrar imagen de ejemplo si no hay una cargada
        if not logo_file:
            st.image("https://img.icons8.com/color/96/000000/company.png", width=100)
        
        # Botón para guardar
        if st.button("Guardar Información de la Empresa", use_container_width=True):
            st.success("Información de la empresa actualizada correctamente.")
    
    with tab4:
        st.markdown("<h2 class='sub-header'>Configuración de Exportación</h2>", unsafe_allow_html=True)
        
        # Opciones de exportación
        st.markdown("<h3>Formatos de Exportación</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>Excel</h4>", unsafe_allow_html=True)
            
            st.checkbox("Incluir gráficos en Excel", value=True)
            st.checkbox("Aplicar formato condicional", value=True)
            st.checkbox("Incluir fórmulas", value=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>PDF</h4>", unsafe_allow_html=True)
            
            st.checkbox("Incluir logo en PDF", value=True)
            st.checkbox("PDF firmado digitalmente", value=False)
            st.checkbox("PDF protegido", value=False)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>Otros Formatos</h4>", unsafe_allow_html=True)
            
            st.checkbox("CSV", value=True)
            st.checkbox("JSON", value=True)
            st.checkbox("XML", value=False)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Plantillas
        st.markdown("<h3>Plantillas de Documentos</h3>", unsafe_allow_html=True)
        
        plantilla_factura = st.file_uploader("Plantilla de factura (DOCX)", type=["docx"])
        plantilla_informe = st.file_uploader("Plantilla de informe financiero (DOCX)", type=["docx"])
        
        # Configuración de envío automático
        st.markdown("<h3>Envío Automático de Informes</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>Informes Periódicos</h4>", unsafe_allow_html=True)
            
            informe_periodico = st.selectbox("Informe", ["Resumen Financiero", "Cuenta de Resultados", "Balance", "Flujo de Caja"])
            periodicidad = st.selectbox("Periodicidad", ["Diario", "Semanal", "Mensual", "Trimestral"])
            destinatarios = st.text_area("Destinatarios (emails separados por comas)")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h4>Programación</h4>", unsafe_allow_html=True)
            
            dia_semana = st.selectbox("Día de la semana", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
            hora = st.time_input("Hora de envío", value=datetime.strptime("08:00", "%H:%M").time())
            
            st.checkbox("Incluir archivos adjuntos", value=True)
            st.checkbox("Enviar incluso si no hay cambios", value=False)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Botón para guardar
        if st.button("Guardar Configuración de Exportación", use_container_width=True):
            st.success("Configuración de exportación guardada correctamente.")

elif opciones == "Ayuda & Soporte":
    st.markdown("<h1 class='main-header'>Ayuda y Soporte</h1>", unsafe_allow_html=True)
    
    # Tabs para diferentes secciones
    tab1, tab2, tab3 = st.tabs(["📚 Guía de Uso", "❓ Preguntas Frecuentes", "🛠️ Soporte Técnico"])
    
    with tab1:
        st.markdown("<h2 class='sub-header'>Guía de Uso</h2>", unsafe_allow_html=True)
        
        # Lista de temas
        temas = [
            "Primeros pasos con el sistema",
            "Gestión de transacciones",
            "Creación y gestión de facturas",
            "Interpretación de informes financieros",
            "Uso de las funciones de IA",
            "Configuración del sistema",
            "Exportación de datos",
            "Gestión de impuestos"
        ]
        
        tema_seleccionado = st.selectbox("Seleccione un tema", temas)
        
        # Mostrar contenido según el tema seleccionado
        if tema_seleccionado == "Primeros pasos con el sistema":
            st.markdown("""
            <div class='card'>
                <h3>Primeros pasos con el sistema</h3>
                
                <h4>1. Configuración inicial</h4>
                <p>Antes de comenzar a utilizar el sistema, es importante configurar los datos básicos de su empresa:</p>
                <ul>
                    <li>Vaya a la sección de "Configuración" → "Empresa"</li>
                    <li>Complete la información fiscal y bancaria</li>
                    <li>Suba el logo de su empresa</li>
                </ul>
                
                <h4>2. Configuración de usuarios</h4>
                <p>Si va a compartir el acceso con otros miembros de su equipo:</p>
                <ul>
                    <li>Vaya a "Configuración" → "Usuarios"</li>
                    <li>Añada usuarios con diferentes roles según sus necesidades</li>
                </ul>
                
                <h4>3. Importar datos iniciales</h4>
                <p>Para empezar con sus datos históricos:</p>
                <ul>
                    <li>Vaya a cada sección (Transacciones, Facturas) y utilice la opción de importar</li>
                    <li>Puede importar desde Excel, CSV o su software contable anterior</li>
                </ul>
                
                <h4>4. Explorar el dashboard</h4>
                <p>El dashboard principal le ofrece una visión general de sus finanzas:</p>
                <ul>
                    <li>Métricas clave: balance, ingresos, gastos</li>
                    <li>Flujo de caja y previsiones</li>
                    <li>Facturas pendientes y próximos vencimientos</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        elif tema_seleccionado == "Uso de las funciones de IA":
            st.markdown("""
            <div class='card'>
                <h3>Uso de las funciones de IA</h3>
                
                <h4>1. Categorización automática de gastos</h4>
                <p>El sistema utiliza inteligencia artificial para categorizar automáticamente sus gastos:</p>
                <ul>
                    <li>Al registrar una nueva transacción, el sistema sugerirá una categoría basada en la descripción</li>
                    <li>Puede aceptar la sugerencia o elegir otra categoría</li>
                    <li>Con el tiempo, el sistema aprende de sus decisiones y mejora la precisión</li>
                </ul>
                
                <h4>2. Predicción de flujo de caja</h4>
                <p>La IA analiza sus patrones históricos para predecir el flujo de caja futuro:</p>
                <ul>
                    <li>En el dashboard, la sección "Análisis Predictivo" muestra la proyección de ingresos y gastos</li>
                    <li>El sistema identifica patrones estacionales y tendencias</li>
                    <li>Las alertas le notificarán si se prevén problemas de liquidez</li>
                </ul>
                
                <h4>3. Recomendaciones financieras</h4>
                <p>Basándose en el análisis de sus datos, el sistema proporciona recomendaciones:</p>
                <ul>
                    <li>Optimización de flujo de caja</li>
                    <li>Identificación de gastos excesivos o irregulares</li>
                    <li>Sugerencias para mejorar la rentabilidad</li>
                </ul>
                
                <h4>4. Mejora continua</h4>
                <p>Las funciones de IA mejoran con el uso:</p>
                <ul>
                    <li>Cuantos más datos registre, mejores serán las predicciones</li>
                    <li>Puede ajustar la sensibilidad de las predicciones en "Configuración" → "Integración con IA"</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h2 class='sub-header'>Preguntas Frecuentes</h2>", unsafe_allow_html=True)
        
        # Preguntas frecuentes con expander
        with st.expander("¿Cómo puedo importar mis datos desde otro sistema?"):
            st.markdown("""
            Para importar datos desde otro sistema:
            
            1. Exporte sus datos del sistema anterior en formato Excel o CSV
            2. Vaya a la sección correspondiente (Transacciones, Facturas, etc.)
            3. Busque el botón "Importar" o similar
            4. Seleccione el archivo y siga las instrucciones para mapear los campos
            
            El sistema admite importación desde la mayoría de formatos comunes y software contable popular como ContaPlus, QuickBooks, Sage, etc.
            """)
            
        with st.expander("¿Es seguro almacenar mis datos financieros en este sistema?"):
            st.markdown("""
            Sí, la seguridad es una prioridad:
            
            - Todos los datos se almacenan cifrados
            - Utilizamos protocolos de seguridad estándar de la industria
            - Las copias de seguridad automáticas protegen contra pérdidas de datos
            - Cumplimos con normativas de protección de datos como RGPD
            
            Además, puede configurar opciones adicionales de seguridad como autenticación de dos factores y restricciones de acceso por IP.
            """)
            
        with st.expander("¿Cómo funciona la categorización automática de gastos?"):
            st.markdown("""
            La categorización automática utiliza inteligencia artificial:
            
            1. Analiza la descripción, importe y otros detalles de la transacción
            2. Compara con patrones aprendidos de transacciones anteriores
            3. Sugiere la categoría más probable
            
            El sistema aprende continuamente de sus correcciones, mejorando la precisión con el tiempo. Si desea entrenar el sistema más rápido, puede ir a "Configuración" → "IA" → "Entrenar categorización" y revisar un conjunto de transacciones para mejorar el modelo.
            """)
            
        with st.expander("¿Qué informes fiscales puedo generar?"):
            st.markdown("""
            El sistema puede generar diversos informes fiscales:
            
            - Declaraciones trimestrales de IVA (modelo 303)
            - Resumen anual de IVA (modelo 390)
            - Retenciones e ingresos a cuenta (modelos 111, 115, 123)
            - Operaciones con terceros (modelo 347)
            - Libro registro de facturas
            
            Los informes se generan en formato oficial o en borrador para facilitar la presentación. En "Informes" → "Impuestos" encontrará todos los informes disponibles.
            """)
            
        with st.expander("¿Puedo acceder al sistema desde dispositivos móviles?"):
            st.markdown("""
            Sí, el sistema es completamente responsive:
            
            - Funciona en cualquier navegador moderno
            - Se adapta a diferentes tamaños de pantalla
            - Disponible como aplicación web progresiva (PWA)
            
            También contamos con aplicaciones nativas para iOS y Android que permiten:
            
            - Escanear facturas y tickets con la cámara
            - Recibir notificaciones de vencimientos
            - Consultar el dashboard y métricas clave
            - Registrar gastos e ingresos en movimiento
            """)
            
        with st.expander("¿Cómo puedo obtener soporte técnico?"):
            st.markdown("""
            Dispone de varias opciones de soporte:
            
            1. **Base de conocimientos**: Consulte nuestra documentación en línea y tutoriales
            2. **Chat en vivo**: Disponible en horario laborable (L-V, 9:00-18:00)
            3. **Email**: Escriba a soporte@finanzas-pymes.com
            4. **Teléfono**: +34 912 345 678 (L-V, 9:00-14:00)
            
            Para problemas urgentes, puede solicitar una llamada prioritaria desde la sección "Soporte Técnico".
            """)
    
    with tab3:
        st.markdown("<h2 class='sub-header'>Soporte Técnico</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Contacte con Soporte</h3>", unsafe_allow_html=True)
            
            nombre_soporte = st.text_input("Su nombre")
            email_soporte = st.text_input("Email de contacto")
            tipo_problema = st.selectbox("Tipo de problema", ["Técnico", "Funcional", "Facturación", "Otros"])
            descripcion = st.text_area("Descripción del problema", height=150)
            archivo = st.file_uploader("Adjuntar capturas o archivos", type=["png", "jpg", "pdf"])
            
            if st.button("Enviar Solicitud", use_container_width=True):
                st.success("Solicitud enviada correctamente. Le responderemos en un plazo de 24 horas laborables.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Información de Contacto</h3>", unsafe_allow_html=True)
            
            st.markdown("""
            <p><b>Email:</b> soporte@finanzas-pymes.com</p>
            <p><b>Teléfono:</b> +34 912 345 678</p>
            <p><b>Horario:</b> Lunes a Viernes, 9:00 - 18:00</p>
            
            <h4>Chat en Vivo</h4>
            <p>Nuestro chat está disponible durante el horario de atención.</p>
            """, unsafe_allow_html=True)
            
            if st.button("Iniciar Chat", use_container_width=True):
                st.info("El servicio de chat se abriría en una ventana externa.")
            
            st.markdown("<h4>Solicitar Llamada</h4>", unsafe_allow_html=True)
            
            telefono_llamada = st.text_input("Su teléfono")
            horario_preferido = st.selectbox("Horario preferido", ["Mañana (9:00-13:00)", "Tarde (13:00-18:00)"])
            
            if st.button("Solicitar Llamada", use_container_width=True):
                st.success("Solicitud de llamada registrada. Le llamaremos lo antes posible.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Acceso a recursos
        st.markdown("<h3>Recursos Adicionales</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='card' style='text-align: center;'>
                <h4>Base de Conocimientos</h4>
                <p>Acceda a tutoriales y documentación detallada</p>
                <a href='#'>Ver documentación</a>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='card' style='text-align: center;'>
                <h4>Tutoriales en Video</h4>
                <p>Aprenda con nuestros videos explicativos</p>
                <a href='#'>Ver videos</a>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class='card' style='text-align: center;'>
                <h4>Comunidad de Usuarios</h4>
                <p>Comparta experiencias con otros usuarios</p>
                <a href='#'>Acceder al foro</a>
            </div>
            """, unsafe_allow_html=True)

# Añadir una nota a pie de página
st.markdown("""
<div style='text-align: center; margin-top: 30px; padding: 20px; color: #666;'>
    <p>Sistema de Contabilidad para PYMEs con IA © 2025</p>
    <p>Desarrollado con tecnología de IA para automatización contable</p>
    <p>Versión 1.0.0</p>
</div>
""", unsafe_allow_html=True)
