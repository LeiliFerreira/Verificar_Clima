import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import customtkinter
import requests
import datetime
import json
import pytz
from datetime import datetime
import pycountry_convert as pc

cor_0 = "#444466"
cor_1 = "#ffffff"
cor_2 = "#6f9fbd"

background_dia= "#6cc4cc"
background_noite= "#484f60"
background_tarde = "#bfb86d"
background = '#ffffff'

janela = Tk()
p1 = PhotoImage(file='img_clima/icone_clima.png')
janela.iconphoto(False, p1)
janela.title("Clima")
janela.geometry("320x350")
janela.configure(bg=background_dia)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

# criando frames...
frame_top= Frame(janela, width=320, height=50, bg=cor_1, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo= Frame(janela, width=320, height=300, bg=background, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, stick=NW)

estilo = ttk.Style(janela)
estilo.theme_use('clam')

global imagem
# Função que retorna as informações...
def informacao():
    chave = 'f3d0d28e586663d7702792b08268796d'
    cidade = e_local.get()

    if (cidade == ""):
        msg = "Informe o local!"
        messagebox.showinfo('Aviso!', msg)
    else:

        api_link = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(cidade, chave)

        r = requests.get(api_link)

        dados = r.json()
        print(dados)

        pais_codigo = dados["sys"]["country"]

        zona_fuso = pytz.country_timezones[pais_codigo]

        pais = pytz.country_names[pais_codigo]

        zona = pytz.timezone(zona_fuso[0])
        zona_horas = datetime.now(zona)
        zona_horas = zona_horas.strftime("%d %m %Y | %H:%M:%S %p")

        tempo = dados['main']['temp']
        pressao = dados['main']['pressure']
        humidade = dados['main']['humidity']
        velocidade = dados['wind']['speed']
        descricao = dados['weather'][0]['description']

    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continente_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continente_codigo)
        return pais_continente_nome

    continente = pais_para_continente(pais)

    # Passando informações nas labels

    l_cidade['text'] = cidade + " - " + pais + " / " + continente
    l_data['text'] = zona_horas
    l_humidade['text'] = humidade
    l_h_simbol['text'] = '%'
    l_h_nome['text'] = 'Humidade'
    l_pressao['text'] = "Pressão : " + str(pressao)
    l_velocidade['text'] = "Velocidade do vento : " + str(velocidade)
    l_descricao['text'] = descricao

    # Trocando o fundo do app...
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")

    global imagem

    zona_periodo = int(zona_periodo)

    if (zona_periodo <= 5):
        imagem = Image.open('img_clima/lua.png')
        background = background_noite

    elif (zona_periodo <= 11):
        imagem = Image.open('img_clima/sol_dia.png')
        background = background_dia

    elif (zona_periodo <= 17):
        imagem = Image.open('img_clima/sol_tarde.png')
        background = background_tarde

    elif (zona_periodo <= 23):
        imagem = Image.open('img_clima/lua.png')
        background = background_noite

    else:
        pass

    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)

    l_icon = Label(frame_corpo, image=imagem, bg=background)
    l_icon.place(x=162, y=50)

    janela.configure(bg=background)
    frame_top.configure(bg=background)
    frame_corpo.configure(bg=background)

    l_cidade['bg'] = background
    l_data['bg'] = background
    l_humidade['bg'] = background
    l_h_simbol['bg'] = background
    l_h_nome['bg'] = background
    l_pressao['bg'] = background
    l_velocidade['bg'] = background
    l_descricao['bg'] = background


# Configurando frame top...
e_local = Entry(frame_top, width=20, justify='left', font=("", 14), highlightthickness=1, relief='solid')
e_local.place(x=15, y=10)

b_ver = customtkinter.CTkButton(frame_top, command=informacao, text='Mostrar',width=10, text_color='#ffffff', fg_color='orange', hover_color= 'grey', text_font=("Ivy 9 bold"))
b_ver.place(x=250, y=10)

# Configurando frame corpo...
l_cidade = Label(frame_corpo, text='',anchor='center', bg=background, fg=cor_1,font=("Arial 14"))
l_cidade.place(x=10, y=4)

l_data = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 10"))
l_data.place(x=10, y=54)

l_humidade = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 45"))
l_humidade.place(x=10, y=100)

l_h_simbol = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 10 bold"))
l_h_simbol.place(x=85, y=110)

l_h_nome = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 8"))
l_h_nome.place(x=85, y=140)

l_pressao = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 10"))
l_pressao.place(x=10, y=184)

l_velocidade = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 10"))
l_velocidade.place(x=10, y=212)

l_descricao = Label(frame_corpo, text='', anchor='center', bg=background, fg=cor_1,font=("Arial 10"))
l_descricao.place(x=170, y=190)

janela.mainloop()