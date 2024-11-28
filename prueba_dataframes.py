import pandas as pd

# Suponiendo que este es el DataFrame original
df = pd.DataFrame({
    'NOMBRE': ['Juan', 'Carlos', 'Miguel', 'Diego', 'Hugo', 'Raúl', 'Jorge', 'Luis', 'Pedro', 'Fernando', 'Gabriel', 'Andrés', 'Ricardo', 'Alejandro', 'Tomás'],
    'APELLIDO': ['Martínez', 'Pérez', 'Sánchez', 'Ramírez', 'Fernández', 'Ortega', 'Mendoza', 'García', 'Morales', 'Vargas', 'López', 'Castillo', 'Hernández', 'Aguilar', 'Torres'],
    'DOCUMENTO': [12345678, 23456789, 34567890, 45678901, 56789012, 67890123, 78901234, 89012345, 90123456, 1234567, 12345001, 23456002, 34567003, 45678004, 56789005],
    'ESPECIALIDAD': ['LAV', 'PDI', 'PIN', 'LAV', 'PDI', 'PIN', 'LAV', 'PDI', 'PIN', 'LAV', 'PDI', 'PIN', 'LAV', 'PDI', 'PIN'],
    'ESPECIALIDAD.1': ['PDI', None, None, None, None, None, 'PDI', None, None, 'PDI', None, None, None, 'LAV', None],
    'ID_TECNICO': ['ntínez123456', 'losez234567', 'uelchez345678', 'goírez456789', 'onández567890', 'lega678901', 'gedoza789012', 'scía890123', 'roales901234', 'nandogas123456', 'rielez123450', 'réstillo234560', 'ardonández345670', 'jandroilar456780', 'ásres567890']
})

print("Datafram original\n",df)
# 1. Eliminar las columnas que contienen la cadena 'ESPECIALIDAD'
df_cleaned = df.loc[:, ~df.columns.str.contains('ESPECIALIDAD')]

# 2. Construir el nuevo DataFrame df_tecnicos_procesos
# Primero obtenemos las columnas 'ESPECIALIDAD', 'ESPECIALIDAD.1', etc.
especialidades_columns = df.columns[df.columns.str.contains('ESPECIALIDAD')]

# Ahora creamos un DataFrame donde concatenamos ID_TECNICO con las especialidades
df_tecnicos_procesos = pd.DataFrame(columns=['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO'])

# Iteramos sobre las columnas de especialidades para generar el nuevo DataFrame
for col in especialidades_columns:
    temp_df = df[['ID_TECNICO', col]].dropna(subset=[col])  # Eliminamos filas con valores nulos en esa especialidad
    temp_df['TEC_PROC'] = temp_df['ID_TECNICO'] + temp_df[col]  # Concatenamos ID_TECNICO y el valor de la especialidad
    temp_df['ID_PROCESO'] = temp_df[col]  # Asignamos el valor de la especialidad a ID_PROCESO
    temp_df = temp_df[['TEC_PROC', 'ID_TECNICO', 'ID_PROCESO']]  # Reordenamos las columnas
    df_tecnicos_procesos = pd.concat([df_tecnicos_procesos, temp_df], ignore_index=True)  # Concatenamos al DataFrame final

# Mostrar los resultados
print("\nDataFrame Limpio (sin las columnas 'ESPECIALIDAD'):")
print(df_cleaned)
print("\nNuevo DataFrame 'df_tecnicos_procesos':")
print(df_tecnicos_procesos)
