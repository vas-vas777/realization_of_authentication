import json
import uuid
import hashlib
import os


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.table_of_users = dict()

    def password_to_hash(self):
        salt = uuid.uuid4().hex
        hash_of_password_with_salt = hashlib.sha256(salt.encode() + self.password.encode())
        return salt + " " + hash_of_password_with_salt.hexdigest()

    def add_new_user(self):
        with open("file.json", "a+") as file:
            if os.stat(file.name).st_size == 0:
                dictionary = {self.name: self.password_to_hash()}
                json.dump(dictionary, file, ensure_ascii=False, indent=3)
                return "Пользователь зарегестрирован"
            else:
                with open("file.json", "r+") as file_json:
                    dict_from_file = json.load(file_json)
                    if self.name in dict_from_file:
                        return "такой уже есть"
                    else:
                        file_json.seek(0)
                        dict_from_file.update({self.name: self.password_to_hash()})
                        json.dump(dict_from_file, file_json, ensure_ascii=False, indent=3)
                        return "Пользователь зарегестрирован"

    def entrance_of_user(self):
        with open("file.json", "r") as file:
            dict_from_file = json.load(file)
            if self.name in dict_from_file:
                salt = dict_from_file.get(self.name).split()[0]
                hash = dict_from_file.get(self.name).split()[1]
                hash_of_password_with_salt = hashlib.sha256(salt.encode() + self.password.encode())
                if hash_of_password_with_salt.hexdigest() == hash:
                    return "Вход успешен"
                else:
                    return "Введен не правильный пароль"
            else:
                return "Такого пользователя нет"

    def change_password(self):
        with open("file.json", "r+") as file:
            dict_from_file = json.load(file)
            if self.name in dict_from_file:
                salt = dict_from_file.get(self.name).split()[0]
                hash = dict_from_file.get(self.name).split()[1]
                hash_of_password_with_salt = hashlib.sha256(salt.encode() + self.password.encode())
                if hash_of_password_with_salt.hexdigest() == hash:
                    temp_password = input("Введите новый пароль: ")
                    passwd = input("Введите новый пароль ещё раз: ")
                    if temp_password == passwd:
                        self.password = passwd
                        file.seek(0)
                        dict_from_file.update({self.name: self.password_to_hash()})
                        json.dump(dict_from_file, file, ensure_ascii=False, indent=3)
                        return "Пароль успешно изменён"
                    else:
                        return "Пароли не совпадают"
                else:
                    return "Введен не правильный пароль"
            else:
                return "Такого пользователя нет"


if __name__ == "__main__":
    while True:
        str = input("Введите 1-(Регистрация) или 2-(Вход), или 3-(Смена пароля), или 0-(Выход из программы): ")
        if str == '1':
            name = input("Введите имя пользователя:")
            password = input("Введите пароль пользователя:")
            user = User(name, password)
            user.add_new_user()
        elif str == '2':
            name = input("Введите имя пользователя:")
            password = input("Введите пароль пользователя:")
            user = User(name, password)
            user.entrance_of_user()
        elif str == '3':
            name = input("Введите имя пользователя:")
            password = input("Введите текущий пароль пользователя:")
            user = User(name, password)
            user.change_password()
        elif str == '0':
            print("Выход")
            break
        elif str != '1' and str != '2' and str != '3':
            print("Не корректный ввод. Выход")
            break
