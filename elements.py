
import copy

fileNameSource = "C:\\PythonDrom\\Tests_2022\\xxxTests\\ANSI_SourceFile.txt"
fileNamePack = "C:\\PythonDrom\\Tests_2022\\xxxTests\\ANSI_PackFile.txt"


# класс личный счёт ======================================================
# ---------- 6 ----------
class Account:
    account = 0

    @staticmethod
    def plusSumm(summ):
        Account.account += summ

    @staticmethod
    def minusSumm(summ):
        Account.account -= summ


    @staticmethod
    # этот статический метод вызывается только при пополнении счёта.
    # Поэтому значение аргумента по умолчанию установлено в '+'
    def addMoney(key='+'):
        summ = 0
        while True:
            try:
                summ = int(input("give the sum for your account >> "))
                # Вопрос о сумме, которая добавляется в Account
                # Прибавление этой суммы в Account
                if key == '+':
                    Account.plusSumm(summ)
                    break
                # Вычитание суммы из Account'а (в коде не используется)
                elif key == '-':
                    Account.minusSumm(summ)
                    break
            except Exception as ex:
                print(ex)

        return Account.account

    # Этот статический метод вызывается из модуля main
    @staticmethod
    def minusMoney(money):
        Account.minusSumm(money)
        return Account.account


# Класс продукты =========================================================

# --------- 5 ----------
class Product:

    # На основе ProdElement (аргумент makeIt) создаётся запись о продукте
    # формата prodPattern.
    # ======================== Формат prodPattern =======================================
    #                "name", "add_rem", "price", "quantity", "full_price", "descriptor"
    #    prodPattern  0       1           2       3           4             5

    @staticmethod
    def makeIt(ProdElement):

        prodObj = {}

        if ProdElement[2] == None:
            ProdElement[2] = 0

        if ProdElement[3] == None:
            ProdElement[3] = 0

        ProdElement[4] = ProdElement[2] * ProdElement[3]

        # реализация формата prodPattern
        prodObj["name"] = ProdElement[0]
        prodObj["add_rem"] = ProdElement[1]
        prodObj["price"] = ProdElement[2]
        prodObj["quantity"] = ProdElement[3]
        prodObj["full_price"] = ProdElement[4]
        prodObj["descriptor"] = ProdElement[5]

        return prodObj

# ========================================================================
# отвечает за формирование списка НАЛИЧНЫХ продуктов и за диалог
# с пользователем: предложение НАЛИЧНЫХ продуктов, предложение пополнения
# счёта (возможна покупка в долг - когда у пользователя продукты
# уже в корзине, а пополнять счёт он не желает), выход из программы.

# ---------- 4 ----------
class ProdManager:

    # реализация ввода-вывода НОВЫМИ СРЕДСТВАМИ: запись-чтение информации о
    # продуктовой корзине в файлы fileNameSource и fileNamePack производятся
    # объектами класса fileMaster.

    f_m = None
    fileNameSource = None
    prodList = None
    products = None


   # Это чтение из файла уже закупленных товаров в список prodList ======

    def readFrom(self):

        while True:

            # чтение строки БЕЗ последнего символа
            p0 = self.f_m.read_FM()[:-1]  # имя

            if p0 == '':  # но возможно не имя, а конец файла
                break     # и на этом цикл прочтения информации из
                          # продуктового файла завершается

            p1 = self.f_m.read_FM()[:-1]  # add/rem
            p2 = self.f_m.read_FM()[:-1]  # цена
            p3 = 0   # количество
            p4 = 0   # полная цена
            p5 = self.f_m.read_FM()[:-1]  # описание
            self.f_m.read_FM()  # читается строка - разделитель

            # здесь из файла методом readline читается по 7 строк.
            # На конце файла возвращается ПУСТАЯ строка.
            # Поэтому для определения конца файла достаточно проверить
            # первую строку. Это делается СРАЗУ после прочтения очередной
            # строки с именем продукта. Уже тогда понятно, что это конец.

            # если файл ещё не прочитан до конца - вызывается статическая
            # функция создания объекта Product и его добавления в список prodList.
            product = Product.makeIt([p0, p1, int(p2), p3, p4, p5])
            # вот этот локальный объект-представитель класса Product
            # применяется при формировании списка prodList
            self.prodList.append(product)

    # ====================================================================
    # в ходе заполнения корзины можно отказаться от ранее выбранного
    # товара. Здесь читается ВЕСЬ список продуктов, влючая как товар для
    # выбора, так и товар для отказа. Записи как для выбора, так и для
    # отказа (покупатель передумал и решил отказаться от выбранного товара)
    # находятся в одном файле. Для покупателя различаются описаниями
    # (вроде как 'взял' - 'отказался'), для программы - значением атрибута
    # add/rem и ценой. Формат записи о товаре в файле ОБЩИЙ
    # (для упрощения процедуры чтения) и нет смысла в записях об удалении
    # из корзины фантазировать со значением цены =========================

    def addToBasket(self):

        print(f'!!!!! addToBasket is here !!!!!')

        # для заполнения корзины прочитывается запись из self.prodList,
        # производится выбор или отказ ранее выбранного
        # (взял и тут же передумал и отказался). Это производится с помощью
        # переменной inBack.
        # нужные товары inBack == yes идут в общий список self.products,
        # ненужные товары inBack == no просто пропускаются, если ранее они
        # НЕ БЫЛИ уже включены в self.products ===========================

        for p in self.prodList:
            inBack = input(f"{p['name']}, {p['descriptor']}, {p['add_rem']} (yes/no) > ")

            if inBack == 'yes':  # добавить товар в корзину (товар нужен 'add')
                                 # выкинуть товар из корзины (товар не нужен 'rem')
                # ========================================================
                print('yes')
                if p['add_rem'] == 'add':  # он для продажи - и он идёт в корзину

                    self.products.append(copy.deepcopy(p))
                # ========================================================
                elif p['add_rem'] == 'rem': # это рекомендация выкинуть товар из корзины (inBack == yes)
                # =======================================================
                    i = 0
                    for pr in self.products:
                        if pr['name'] == p['name']:
                            del self.products[i]
                            break
                        else:
                            i += 1
                    # ====================================================

            elif inBack == 'no': # пропуск записи (годный для продажи товар НЕ нужен)
                print('no')
                if p['add_rem'] == 'add':  # он для продажи, но клиенту не нужен
                    pass
                elif p['add_rem'] == 'rem':  # из корзины этот товар НЕ выкидывать
                    pass

        # содержимое корзины =============================================
        print(self.products)

    # ====================================================================

    def addAccount(self):
        addAcc = "yes"
        while addAcc == 'yes':
            print('add account ...')
            self.account = Account.addMoney()
            addAcc = input(f"do you want to add your account (yes/no) > ")

        print(f'your account is {self.account}')


    # метод меню обеспечивает управление приложением =====================
    def DoIt(self):
        answer = ''
        while answer != '3':
            print(f'ProdManager 1: пополнить счёт')
            print(f'ProdManager 2: добавить в корзину')
            print(f'ProdManager 3: хватит выбирать')
            print(f'ProdManager 4: кончать работу')


            answer = input('>>> ')
            if answer == "1":
                print("answer == 1, Account.addMoney")
                self.account = Account.addMoney('+')
                # пополнение счёта есть ДОБАВЛЕНИЕ

            elif answer == "2":
                print("answer == 2, self.addToBasket")
                self.addToBasket()   # поместить товары в корзину

            elif answer == "3":
                print("answer == 3, return to the PersonalAccount")
                return False     # это возвращение в PersonalAccount

            elif answer == "4":
                print("answer == 4, the end of job")
                return False    # это конец работы
            else:
                print("incorrect answer") # непонятно, что это было

    # ====================================================================

    def __init__(self, nameSource, fileMaster):

        print('ProdManager...__init__')
        self.products = list()
        self.prodList = list()

        self.fileNameSource = nameSource
        self.f_m = fileMaster   # этот аргумент есть ссылка на объект -
        # представитель класса fileMaster(!!!). Здесь у него то же имя,
        # что и у класса fileMaster. Но конечно же это НЕ класс.

        self.readFrom()

# ========================================================================
# класс fileMaster реализует чтение-запись в входные и выходные файлы приложения.
# ВЕСЬ ввод-вывод в приложении реализован ТОЛЬКО через объекты этого класса.
# обращение к инициализатору сопровождается закрытием ранее открытого файла,
# затем осуществляется повторное открытие файла на чтение или запись.
# После этого осуществляется вызов соответствующего метода: write_FM либо read_FM.

# ---------- 2 ----------
class fileMaster:

    fm=None

    def __init__(self, file, mode):

        if self.fm != None:
            self.fm.close()

        self.fm = open(file,
                      mode,
                      buffering=-1,
                      encoding=None,
                      errors=None,
                      newline=None,
                      closefd=True,
                      opener=None)

    def write_FM(self, strKey):
        self.fm.write(strKey)

    def read_FM(self):
        return(self.fm.readline())






