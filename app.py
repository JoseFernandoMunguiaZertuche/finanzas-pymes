import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finanzas PYMEs", layout="wide")

st.title("Sistema de Contabilidad para PYMEs")
st.subheader("Dashboard de demostración")

# Sidebar
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Dashboard", "Transacciones", "Facturas", "Informes"])

if page == "Dashboard":
    # Display mock data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Balance Total", "15.243,00 €", "8.5%")
    with col2:
        st.metric("Ingresos (Mes)", "8.759,42 €", "12.3%")
    with col3:
        st.metric("Gastos (Mes)", "5.345,18 €", "-3.4%")
    with col4:
        st.metric("Próximos Impuestos", "2.154,33 €", "")
    
    # Mock chart
    st.subheader("Flujo de Caja")
    chart_data = pd.DataFrame({
        'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        'Ingresos': [12000, 19000, 15000, 17000, 16000, 23000, 25000, 21000, 22000, 24000, 19000, 18000],
        'Gastos': [10000, 12000, 13000, 15000, 14000, 15000, 16000, 17000, 18000, 19000, 16000, 15000]
    })
    chart_data = chart_data.melt('Mes', var_name='Tipo', value_name='Cantidad')
    st.line_chart(chart_data, x='Mes', y='Cantidad', color='Tipo')
    
    # Expenses by category
    st.subheader("Gastos por Categoría")
    categories = ['Suministros', 'Alquiler', 'Salarios', 'Marketing', 'Software', 'Otros']
    values = [4000, 7000, 15000, 3000, 2000, 1000]
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%')
    st.pyplot(fig)

elif page == "Transacciones":
    st.header("Registro de Transacciones")
    st.write("Aquí podrá ver y gestionar todas sus transacciones financieras.")
    
elif page == "Facturas":
    st.header("Gestión de Facturas")
    st.write("Aquí podrá crear, ver y gestionar todas sus facturas.")
    
elif page == "Informes":
    st.header("Informes Financieros")
    st.write("Aquí podrá generar informes y análisis financieros.")
