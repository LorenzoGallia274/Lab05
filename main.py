import flet as ft
from flet import MainAxisAlignment

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    # TextField per i 3 parametri necessari ad aggiungere un nuovo strumento
    TipoField = ft.TextField(label='Tipo')
    MarcaField = ft.TextField(label='Marca')
    AnnoField = ft.TextField(label='Anno acquisto')
    # TextField per lo zero al centro del contatore
    # imposto la larghezza, la grandezza del testo e l'allineamento centrale
    myText = ft.TextField(value='0', disabled = True, width = 100, text_size = 30, text_align = ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    # gestisce la logice del plus: incrementa il prezzo mostrato a schermo
    def handler_plus(e):
        # converte in intero per poter incrementare
        v = int(myText.value)
        v+=1
        # lo riconverto in stringa e lo assegno al value di MyText
        myText.value = str(v)
        myText.update()

    # gestisce la logice del minus: decrementa il prezzo mostrato a schermo
    def handler_minus(e):
        # converte in intero per poter decrementare
        v = int(myText.value)
        v-=1
        # lo riconverto in stringa e lo assegno al value del testo
        myText.value = str(v)
        myText.update()
    # creo i pulsanti per il plus e minus, collegandoli al loro rispettivo handler al click (on_click)
    myBtnMinus = ft.IconButton(icon=ft.Icons.REMOVE, icon_size=30, on_click=handler_minus, icon_color = 'Red')
    myBtnPlus = ft.IconButton(icon=ft.Icons.ADD, icon_size=30, on_click=handler_plus, icon_color = 'Green')
    # definisco la funzione aggiungi_strumento che gestisce il salvataggio di un nuovo strumento
    def aggiungi_strumento(e):
        # gestione eccez.
        # blocco try
        try:
            # provo a convertire in interi l'anno e il prezzo inseriti nel testo dei due campi
            anno_conv = int(AnnoField.value)
            valore_conv = int(myText.value)
        except:
            # se ad esempio l'utente digita lettere nell'anno...
            # mostra un messaggio di errore
            alert.show_alert("Errore: inserisci valori numerici validi per anno e posti")
            # interrompe la funzione (non salva dati errati)
            return
        # richiamo il metodo per aggiungere il nuovo strumento al deposito
        deposito.aggiungi_strumento(TipoField.value, MarcaField.value, anno_conv, valore_conv)
        # svuoto i campi per essere pronti ad inserire nuovi strumenti
        TipoField.value = ''
        MarcaField.value = ''
        AnnoField.value = ''
        # azzero il contatore
        myText.value = '0'
        # richiamo la funzione che svuota e ricrea la ListView degli strumenti
        aggiorna_lista_strumenti()
        page.update()




    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    # creo il pulsante per aggiungere un nuovo strumento, collegato al click (on_click) ad aggiungi_strumento
    BtnAggiungi = ft.Button('Aggiungi strumento', on_click = aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        # 'riprendo' lo stile di layout delle altre sezioni
        ft.Divider(),
        ft.Text('Aggiungi nuovo strumento', size = 20),
        # prima riga
        ft.Row(controls=[TipoField, MarcaField, AnnoField, myBtnMinus, myText, myBtnPlus], alignment = ft.MainAxisAlignment.CENTER),
        # seconda riga
        ft.Row(controls=[BtnAggiungi],alignment = ft.MainAxisAlignment.CENTER),





        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
