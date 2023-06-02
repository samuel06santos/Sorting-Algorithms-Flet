from flet import *
from time import sleep
from operator import attrgetter
from random import sample

class Barra(Container):
    def __init__(self, height:int|float=10) -> None:
        super().__init__()
        self.bgcolor = colors.YELLOW
        self.height = height
        self.width = 10
    def __lt__(self, other):
        return self.height < other.height
    def __le__(self, other):
        return self.height <= other.height

class SortAlg(UserControl):
    def __init__(self, page:Page) -> None:
        super().__init__()
        self.page = page
        self.barras = self.create_bars()
        self.row_barras:Row = Row(
            alignment= MainAxisAlignment.CENTER,
            vertical_alignment= CrossAxisAlignment.END, 
            spacing= 3,
            controls=
                self.barras
            )


    def create_bars(self) -> list[Barra]:
        bars = []
        for e, _height in enumerate(sample(range(10,200,5),38)):
            bars.insert(e, Barra(_height) )
        return bars
    
    def new_bars(self):
        self.row_barras.controls = self.create_bars()
        self.row_barras.update()

    def play(self, e):
        self.executando.data = True
        self.page.update()
        self.verifica()

    def verifica(self):
        print(self.executando.data)

    def stop(self, e):
        self.executando.data = False
        self.executando.update()
        self.verifica()


    def build(self):
        self.executando:Text = Text(data=True)
        self.velocidade:Text = Text(data = 1000, value= f"Delay 1000ms")
        self.Play_Button: ElevatedButton = ElevatedButton(content=Icon(icons.PLAY_ARROW), on_click=self.play, disabled=True)
        self.Stop_Button: ElevatedButton = ElevatedButton(content=Icon(icons.STOP), on_click=self.stop, disabled=True)
        return \
            Container(content=
                Column([
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text("Sorting Algorithms", size=40),
                            Text("BETA", size=26, bgcolor=colors.RED, height=60)
                        ]
                    ),
                    Row(
                        alignment= MainAxisAlignment.CENTER,
                        spacing= 6,
                        controls=[
                            ElevatedButton("BubbleSort", height=40, on_click=lambda _: self.BubbleSort()),
                            ElevatedButton("InsertionSort", height=40, on_click=lambda _: self.InsertionSort()),
                            ElevatedButton("SelectionSort", height=40, on_click=lambda _: self.SelectionSort()),
                            ElevatedButton("QuickSort", height=40, on_click=lambda _: self.QuickSort(), disabled=True),
                            ElevatedButton("MergeSort", height=40, on_click=lambda _: self.MergeSort(), disabled=True)
                        ]
                    ),
                    Row(
                        alignment= MainAxisAlignment.END,
                        spacing= 6,
                        controls= [
                            self.Play_Button,
                            self.Stop_Button,
                            ElevatedButton("+", on_click=self.more_vel),
                            ElevatedButton("-", on_click=self.minus_vel),
                            ElevatedButton(content=Icon(icons.REPEAT), on_click=lambda _:self.new_bars()) # repeat_btn
                        ]
                    ),
                    Row(alignment=MainAxisAlignment.END, controls=[self.velocidade]),
                    self.row_barras,
                    self.executando
                ]) # Column
            ) # Container
            
    
    def more_vel(self, e):
        max = 0.001
        vel_atual = self.velocidade.data/10 if self.velocidade.data > max else max
        self.velocidade.data = vel_atual
        self.velocidade.value = f"Delay {vel_atual}ms"
        self.velocidade.update()

    def minus_vel(self, e):
        max = 1000
        vel_data = self.velocidade.data
        vel_atual = vel_data*10 if vel_data not in [max,1000.0] else max

        self.velocidade.data = vel_atual
        self.velocidade.value = f"Delay {vel_atual}ms"
        self.velocidade.update()

    def freio(self):
        if not self.executando.data:
            return sleep(20)

    def completed(self, lista):
        for b in lista:
            b.bgcolor = colors.GREEN
        self.row_barras.update()

    n_max = lambda _bars: max(_bars, key=attrgetter('height'))

    def BubbleSort(self):
        bars = self.row_barras.controls
        n = len(bars)
        for i in range(n-1):
            for j in range(0, n-i-1):
                self.freio()
                if bars[ j ] > bars[ j+1 ]:
                    bars[j].bgcolor = colors.RED
                    self.row_barras.update()
                    bars[ j ], bars[ j+1 ] = bars[ j+1 ], bars[ j ]
                    self.row_barras.update()
                    sleep(self.velocidade.data/1000)
                self.row_barras.update()
            self.freio()

        self.completed(bars)

    def InsertionSort(self):
        bars = self.row_barras.controls
        n = len(bars)
        for i in range(1, n):
            self.freio()
            key = bars[ i ]
            j = i - 1
            while j >= 0 and key < bars[ j ]:
                self.freio()
                bars[ j+1 ], bars[ j ] = bars[ j ], bars[ j+1 ]
                bars[ j+1 ].bgcolor = colors.RED
                j -= 1
                self.row_barras.update()
                sleep(self.velocidade.data/1000)
            bars[ j+1 ] = key
            self.row_barras.update()
        self.completed(bars)
        
    def SelectionSort(self):
        bars = self.row_barras.controls
        n = len(bars)
        for i in range(n):
            min_idx, aux = i, i
            bars[ aux ].bgcolor = colors.GREEN
            self.row_barras.update()

            for j in range( i+1 , n):
                self.freio()
                bars[ j ].bgcolor = colors.RED
                self.row_barras.update()
                sleep(self.velocidade.data/2000)

                if bars[ j ] < bars[ min_idx ]:
                    bars[ min_idx ].bgcolor = colors.YELLOW
                    min_idx = j
                    bars[ j ].bgcolor = colors.ORANGE

                else:
                    bars[ j ].bgcolor = colors.YELLOW
                self.row_barras.update()
            
            bars[ i ], bars[ min_idx ] = bars[ min_idx ], bars[ i ]
            bars[ i ].bgcolor = colors.RED
            self.row_barras.update()
            sleep(self.velocidade.data/2000)
        self.completed(bars)

    def QuickSort(self):
        bars = self.row_barras.controls
        if len(bars) <= 1:
            return bars
        else:
            pivo = bars[0]
            esquerda = [ x for x in bars[1:] if x < pivo ]
            direita = [ x for x in bars[1:] if x > pivo ]
            self.row_barras.update()
            sleep(self.velocidade.data/1000)
            return self.QuickSort(esquerda) + [pivo] + self.QuickSort(direita)
            
    # QuickSort

    def MergeSort(self):
        bars = self.row_barras.controls
        def merge(arr, l, m, r):
            n1 = m - l + 1
            n2 = r - m

            L = [0] * (n1)
            R = [0] * (n2)

            for i in range(0, n1):
                L[i] = arr[l + i]

            for j in range(0, n2):
                R[j] = arr[m + 1 + j]

            i = j = 0
            k = l

            while i < n1 and j < n2:
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    arr[k].bgcolor = colors.RED
                    self.row_barras.update()
                    sleep(self.velocidade.data/4000)
                    i += 1
                else:
                    arr[k] = R[j]
                    arr[k].bgcolor = colors.RED
                    self.row_barras.update()
                    sleep(self.velocidade.data/4000)
                    j += 1
                k += 1

            while i < n1 and self.freio:
                arr[k] = L[i]
                arr[k].bgcolor = colors.RED
                self.row_barras.update()
                sleep(self.velocidade.data/4000)
                i += 1
                k += 1

            while j < n2 and self.freio:
                arr[k] = R[j]
                arr[k].bgcolor = colors.RED
                self.row_barras.update()
                sleep(self.velocidade.data/4000)
                j += 1
                k += 1

        def mergeSort(arr, l, r):
            if l < r and self.freio:
                m = l+(r-l)//2

                mergeSort(arr, l, m)
                mergeSort(arr, m+1, r)
                merge(arr, l, m, r)

        mergeSort(bars, 0, len(bars)-1)
        self.completed(bars)
        self.page.update()

    # MergeSort()
