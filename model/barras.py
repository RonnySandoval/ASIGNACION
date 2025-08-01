
df = 30    
h_disp = 700
items = len(df)
num_bar = h_disp / 50


if num_bar <= 5:
    h_plot = items * 100
elif 5 < num_bar <= 10 and items < num_bar:
    h_plot = items * 90
elif 5 < num_bar <= 10 and items >= num_bar:
    h_plot = items * 80
elif 10 < num_bar <= 15 and items < num_bar:
    h_plot = items * 70
elif 10 < num_bar <= 15 and items >= num_bar:
    h_plot = items * 60
else:
    h_plot = items * 50

MIN_ALTURA_BARRA = 50
MAX_ALTURA_BARRA = 100
altura_por_barra = max(MIN_ALTURA_BARRA, min(MAX_ALTURA_BARRA, h_disp // items))
h_plot = items * altura_por_barra