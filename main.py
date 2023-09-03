# программа 'Личный счёт':
#
# Пользователь запускает программу у него на счету 0 руб
# Программа предлагает следующие варианты действий (основное меню):
#
# - пополнить счет (при выборе этого пункта пользователю предлагается ввести
# сумму на сколько пополнить счет, после того как пользователь вводит сумму
# она добавляется к счету и снова переходит в основное меню)

# - совершить покупку (при выборе этого пункта программа предлагает пользователю
# ввести сумму покупки, если она больше количества денег на счете, то сообщается,
# что денег не хватает, после чего программа переходит в основное меню.
# Если денег достаточно, программа предлагает пользователю ввести название покупки,
# например (одежда и обувь), снимает деньги со счета пользователя, сохраняет
# покупку в истории покупок, и переходит в основное меню)
#
# - история покупок (программа выводит историю покупок пользователя - название и сумму,
# и переходит в основное меню)

# - выход (завершение цикла, выход из меню)
#
# Особенности реализации программы.
# - пополнение (и дополнение) счёта производится:
#     непосредственно после запуска программы,
#     при выборе пункта меню,
#     в ситуации, когда сумма на счету превосходит сумму, которая была потрачена

# - при отказе пополнить счёт выполнение программы прекращается.

# - имеется 'список продуктов' - C:\PythonDrom\Tests_2022\xxxTests\sourceFile.txt.
#     это описание того, что имеется на складе там же список продуктов, от которых
#     можно отказаться при выборе (покупатель выбрал товар, положил в корзинку,
#     передумал и выкинул). Это возможно, если товар ЕЩЁ НЕ БЫЛ ОПЛАЧЕН. При
#     отказе от товара из списка выбранных покупателем товаров выбирается и
#     удаляется первый из ранее выбранных (найденных в корзине) товаров.
#
# - по соответствующему пункту меню (хватит выбирать) производится окончательное
#   оформление покупки (из корзины выкидываются товары, от которых покупатель
#   отказался), уточнение количества выбранного товара, расчёт общей стоимости
#   корзины, возможно, предложение о пополнении счёта.
#
# - выход в главное меню с возможность пополнения корзины и прочей суетой,
#   предусмотренной в программе.
#
# - при завершении работы (выход из программы при отказе пополнения счёта
#   или выборе соответствующего пункта меню) в файл
#   C:\PythonDrom\Tests_2022\xxxTests\pacFile.txt записывается история
#   покупки, которая обновляется при очередном запуске программы.




from elements import Account

from elements import ProdManager
from elements import fileMaster  # класс для реализации чтения-записи в
                                 # файлы для реализации алгоритмов личного счёта

from elements import fileNameSource
from elements import fileNamePack


# ========================================================================

# ---------- 3 ----------
# Класс ConvenienceFood - продукты, готовые к употреблению ===============
class ConvenienceFood:

    prodQuantity = 0
    result = 0
# ========================================================================
    # Свойство применяется для выбранных товаров из списка
    # PersonalAccount.xFood. Здесь важны как setter,
    # так и property свойства. В property (атрибут result) этого свойства
    # записывается информация о результате применения свойства. И эту информацию
    # можно получить БЕЗ каких-либо дополнительных действий
    # (просто обратившись к property свойства) ===============================
    @property
    def qQuantity(self):
        print(' <<<<< ConvenienceFood: property qQuantity is here')
        return self.prodQuantity

    @qQuantity.setter
    def qQuantity(self, product):
        print('>>>>> ConvenienceFood: qQuantity.setter is here')
        while True:
            # количество товара ПОКА спрашивается для товара,
            # от которого сразу не отказались и возможно, НЕ откажутся.
            # Для записей отказа  количество возвращаемого товара ПОКА не
            # принципиально. Всё равно удаляется первая встреченная в
            # в списке запись.
            if product['add_rem'] == 'add':
                pq = input(f"give the quantity of product {product['name']}, {product['price']} >> ")
                try:
                    self.prodQuantity = int(pq)
                except Exception as e:
                    print(e)
                else:
                    break
            else:
                self.prodQuantity = 0

        product['quantity'] = self.prodQuantity

    # =====================================================================
    @property
    def fFood(self):
        print(f'fFood {self.result}')
        return self.result

    @fFood.setter
    def fFood(self, product):
        print(f"fFood.setter: product={product}")
        if product["add_rem"] == 'add':
            PersonalAccount.xFood.append(product)
            self.result = product['name'] + ' append: success'

        elif product["add_rem"] == 'rem':
            for xf in PersonalAccount.xFood:
                if xf["name"] == product["name"]:
                    try:
                        PersonalAccount.xFood.remove(xf)
                        self.result = product['name'] + ' remove: success'
                    except:
                        self.result = product['name'] + ' remove: fall'

            if product["add_rem"] == 'rem':
                try:
                    PersonalAccount.xFood.remove(product)
                    try:
                        self.result += product['name'] + ' (add_rem) remove: success'
                    except:
                        self.result = ' (add_rem) remove: success'
                except:
                    try:
                        self.result += product['name'] + ' (add_rem) remove: fall'
                    except:
                        self.result = ' (add_rem) remove: fall'

# ========================================================================
# Метод FoodFormer добавляет и удаляет (если сможет!) продукты из списка
# PersonalAccount.xFood. Метод также возвращает информацию о результатах
# применения в качестве возвращаемого значения и её надо
# дополнительно перехватить и сохранить как значение переменной.
# И в чём разница между методом и свойством?
# Метод (обычный) - один и НАДО специально получить и сохранить
# результат его выполнения в качестве значения переменной.
# Свойство - два метода (get, set) и НЕ НАДО специально сохранять
# результатов выполнения метода set.
# Хотя этот результат вытолнения set фиксируется в get
# (чем не возвращаемое значение обычного метода?)
# ========================================================================

    def FoodFormer(self, product):

        print(f'FoodFormer({product})')

        if product['add_rem'] == 'add':
            PersonalAccount.xFood.append(product)
            self.result = product['name'] + ' append: success'

        # отказ от ранее выбранного товара
        # (из PersonalAccount.xFood удаляется ПЕРВАЯ встреченная запись)
        # при отказе от ранее оплаченного товара деньги НЕ ВОЗВРАЩАЮТСЯ.
        elif product['add_rem'] == 'rem':
            for xf in PersonalAccount.xFood:
                if xf['name'] == product['name']:
                    try:
                        PersonalAccount.xFood.remove(xf)
                        self.result = product['name'] + ' remove: success'
                    except:
                        self.result = product['name'] + ' remove: fall'

            if product["add_rem"] == 'rem':
                try:
                    PersonalAccount.xFood.remove(product)
                    try:
                        self.result += product['name'] + ' (add_rem) remove: success'
                    except:
                        self.result = ' (add_rem) remove: success'
                except:
                        try:
                            self.result += product['name'] + ' (add_rem) remove: fall'
                        except:
                            self.result = ' (add_rem) remove: fall'

        return self.result

# ========================================================================

    # инициализатор объекта класса ConvenienceFood.
    # self.result единственный атрибут объекта класса
    def __init__(self):
        print('__________ this is ConvenienceFood initor __________')
        self.result = None
        self.prodQuantity = None

    # ====================================================================

# ---------- 1 ----------
class PersonalAccount:

    xFood = []
    fMaster = None
    prodManager = None
    convenienceFood = None


    def writeIN(self):

        try:
            self.fMaster = fileMaster(fileNamePack, "x")
            # создать файл и открыть его на запись либо сгенерировать исключение
            # FileExistsError, если файл с таким именем уже существует.
        except FileExistsError:
            self.fMaster = fileMaster(fileNamePack, "a")
            # открыть файл на дозапись (содержимое файла не удаляется,
            # а запись новой информации осуществляется в конец файла).

        for xf in self.xFood: #self.personalAccount.xFood:
            # запись в файл выбранных и оплаченных товаров
            self.fMaster.write_FM(
                xf['name'] + '\n' +
                xf['add_rem'] + '\n' +  # здесь это поле всегда 'add'
                str(xf['price']) + '\n' +
                str(xf['quantity']) + '\n' +
                str(xf['full_price']) + '\n' +
                xf['descriptor'] + '\n' +
                ' ' + '\n'
            )

    # ====================================================================

    # выбор продуктов: метод FoodMaster ==================================

    def FoodMaster(self):
        print('>>> FoodMaster <<<')

        i = 0
        for prod in self.prodManager.products:
            print(f'{i} ' + prod['name'])
            i += 1

        # кидает товары из prodManager.products в self.xFood =============
        for prod in self.prodManager.products:
            print(f'to convenienceFood.FoodFormer({prod})')
            self.convenienceFood.FoodFormer(prod)


        self.prodManager.products = list()

        # для каждого товара из self.xFood
        # декоратором self.qQuantity определяется количество
        # выбранного товара, цена товара изначально заложено в его описании
        # и представляет собой атрибут объекта. Получить информацию о
        # цене товара очень просто.
        for xF in self.xFood:
            self.convenienceFood.qQuantity = xF     # декораторм определяется количество товара
            prod["quantity"] = self.convenienceFood.qQuantity  # количество товара
            prod["full_price"] = xF["price"] * xF["quantity"]
            print(f'~~~~~ {prod["name"]} quantity:{prod["quantity"]}   price:{prod["price"]} ~~~~~')


        self.writeIN()  # Это ЗАПИСЬ в файл ===========================

        print()

       # ====================================================================

    def DoIt(self):

        print(f'>>>>> pa.DoIt <<<<<')

        # из объекта представителя класса PersonalAccount открыть счёт
        # и с помощью статического метода addMoney класса Account
        # пополнить счёт
        self.prodManager.account = Account.addMoney('+')
        print(f"personal account is open: {self.prodManager.account}")
        # и посмотреть результат пополнения ==============================

        go = True
        while go:

            # ================================================================
            print('to prodManager.DoIt...')
            go = self.prodManager.DoIt()  # запуск менеджера по закупкам продуктов

            #!!!if go == True:
            print('***********************************************')
            print(f'current account {self.prodManager.account}')
            print()

            # состояние корзины: выбранные товары и записи о возможных отказах
            print('products')
            i = 0
            j = 0
            for prod in self.prodManager.products:
                if prod['add_rem'] == 'add':      # выбранные товары
                    print(f' + {i}: {prod}')
                    i += 1
                elif prod['add_rem'] == 'rem':    # отказы от товара
                    print(f' - {j}: {prod}')
                    j += 1

            print('***********************************************')

            print('_____ to FoodMaster() _____')
            self.FoodMaster()   # на основе элемента списка fmFood
                                # строится список self.xFood

            fP = 0
            for xf in self.xFood:
                fP += int(xf['full_price'])   # сумма на счету

            print(f'full Price is {fP}, prodManager.account is {self.prodManager.account}')
            self.prodManager.account = Account.minusMoney(fP)  # изменение счёта
                                                                # (статический метод класса Account)
            print(f'\nfull Price :  account\n{fP}              {self.prodManager.account}')

            if self.prodManager.account < 0:
                # если всё потрачено - предложение пополнить счёт
                while True:
                    answer = input("do you want to top up your account ? (yes/no) >> ")
                    if answer == 'yes':
                        self.prodManager.account = Account.addMoney('+')
                        print(f'purchase is {self.prodManager.account}')
                        break
                    elif answer == 'no':
                        go = False
                        break
                    else:
                        print(f'{answer} is incorrect answer (yes/no) only')

            else:
                go = False

            print("personal account is close")


        # ================================================================
        # При выходе из менеджера определён размер счёта клиента
        # и список товаров, выбранных клиентом. По факту это корзина, в которую
        # клиент накидал товаров. Эти товары из корзины оплачиваются
        # клиентом из его текущего счёта
        print('prodManager was here')


    # инициализация объекта, представляющего класс PersonalAccount. ======

    # конструктор объекта PersonalAccount ================================
    def __init__(self, nameSource):

        self.fMaster = fileMaster(nameSource, 'r')                      # объект fileMaster
        print(f'~~~~~~~~~~ fileMaster = {nameSource} ~~~~~~~~~~')
        self.prodManager = ProdManager(nameSource, self.fMaster)        # объект ProdManager
        print('to ConvenienceFood initor')
        self.convenienceFood = ConvenienceFood()                        # объект ConvenienceFood
        print(f'ConvenienceFood was here {self.convenienceFood}')

# ========================================================================
def main(fnSource):

    pa = PersonalAccount(fnSource)
    #                 имена файлов fileMaster'а
    pa.DoIt()         # объекту PersonalAccount работать!

if __name__ == '__main__':
    main(fileNameSource)


