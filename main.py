from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Arial"
FONT_SIZE = 15

# ---------------------------- SEARCHING FOR PASSWORD ------------------------------- #


def find_password():
    website = website_label_entry.get().lower()
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            # messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\n"
            #                                            f"Password : {data[website]['password']}")
            password_label_entry.delete(0, 'end')
            email_username_label_entry.delete(0, 'end')
            password_label_entry.insert(0, data[website]['password'])
            email_username_label_entry.insert(0, data[website]['email'])

        else:
            messagebox.showinfo(title="Error", message=f"No data for '{website}'")
            password_label_entry.delete(0, 'end')
            email_username_label_entry.delete(0, 'end')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_label_entry.delete(0, 'end')
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    # pyperclip.copy(password)

    password_label_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_label_entry.get().lower()
    email = email_username_label_entry.get()
    password = password_label_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or password == "" or email == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                if website in data:
                    messagebox.showinfo(title="Oops", message=f"Data for '{website}' already exists.")

                    website_label_entry.delete(0, 'end')
                    password_label_entry.delete(0, 'end')
                    email_username_label_entry.delete(0, 'end')

                    password_label_entry.insert(0, data[website]['password'])
                    website_label_entry.insert(0, website)

                else:
                    data.update(new_data)
                    website_label_entry.delete(0, 'end')
                    password_label_entry.delete(0, 'end')
                    email_username_label_entry.delete(0, 'end')

                    messagebox.showinfo(title="Success", message=f"Data for '{website}' added.")
                    website_label_entry.focus()

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)

        except:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)


# ---------------------------- DELETE PASSWORD ------------------------------- #

def delete_password():
    website = website_label_entry.get().lower()
    email = email_username_label_entry.get()
    password = password_label_entry.get()
    new_data = {}
    if website == "" or password == "" or email == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                if website not in data:
                    messagebox.showinfo(title="Oops", message=f"Data for '{website}' does not exists.")
                else:
                    if messagebox.askyesno(title="Are you sure?", message=f"Are you sure you want delete data for "
                                                                          f"'{website}'?"):

                        for el in data:
                            if el != website:
                                old_data = {
                                    el: {
                                        "email": data[el]['email'],
                                        "password": data[el]['password'],
                                    }
                                }
                                new_data.update(old_data)

                        with open("data.json", "w") as f:
                            json.dump(new_data, f, indent=4)
                        messagebox.showinfo(title="Success", message=f"Data for '{website}' deleted.")
                        website_label_entry.delete(0, 'end')
                        password_label_entry.delete(0, 'end')
                        email_username_label_entry.delete(0, 'end')
                        website_label_entry.focus()


        except:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)
# ---------------------------- COPY PASSWORD ------------------------------- #


def copy_password():
    password = password_label_entry.get()
    if password != "":
        pyperclip.copy(password)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=10, pady=10, bg="#C6D8FF")
window.title("Password Manager")
window.iconbitmap('logo/icon.ico')
logo = PhotoImage(file="logo/logo2.png")
canvas = Canvas(width=200, height=200, bg="#C6D8FF", highlightthickness=0)
canvas.create_image(100, 100, image=logo)

website_label_img = PhotoImage(file="labels/website_label.png")
email_username_label_img = PhotoImage(file="labels/email_label.png")
password_label_img = PhotoImage(file="labels/password_label.png")

website_label = Label(text="Website:", font=(FONT_NAME, FONT_SIZE, "bold"), image=website_label_img, bd=0, pady=1)
email_username_label = Label(text="Email/Username:", font=(FONT_NAME, FONT_SIZE, "bold"),
                             image=email_username_label_img, bd=0, padx=1)
password_label = Label(text="Password:", font=(FONT_NAME, FONT_SIZE, "bold"), image=password_label_img, bd=0, pady=1)

website_label_entry = Entry(width=36, font=FONT_NAME, bd=0)
website_label_entry.focus()
email_username_label_entry = Entry(width=36, font=FONT_NAME, bd=0)
password_label_entry = Entry(width=36, font=FONT_NAME, bd=0)

generate_button_img = PhotoImage(file="buttons/generate_button.png")
search_button_img = PhotoImage(file="buttons/search_button.png")
add_button_img = PhotoImage(file="buttons/add_button.png")
delete_button_img = PhotoImage(file="buttons/delete_button.png")
copy_button_img = PhotoImage(file="buttons/copy_button.png")

generate_password_button = Button(text="Generate password", command=generate_password, width=220,
                                  activebackground='#C6D8FF', relief=RIDGE, fg='white', image=generate_button_img,
                                  borderwidth=0,
                                  cursor="hand2", bg="#C6D8FF")
add_button = Button(text="Add", command=save, width=220, activebackground='#C6D8FF',
                    relief=RIDGE, fg='white', image=add_button_img, borderwidth=0, cursor="hand2", bg="#C6D8FF")

delete_button = Button(text="Delete", command=delete_password, width=220, activebackground='#C6D8FF',
                       relief=RIDGE, fg='white', image=delete_button_img, borderwidth=0, cursor="hand2", bg="#C6D8FF")

copy_password = Button(text="Copy", command=copy_password, width=220, activebackground='#C6D8FF',
                       relief=RIDGE, fg='white', image=copy_button_img, borderwidth=0, cursor="hand2", bg="#C6D8FF")

search_button = Button(text="Search", command=find_password, width=220, activebackground='#C6D8FF',
                       relief=RIDGE, fg='white', image=search_button_img, borderwidth=0, cursor="hand2", bg="#C6D8FF")

canvas.grid(column=1, row=0, pady=5)
website_label.grid(column=0, row=1, padx=7)
email_username_label.grid(column=0, row=2, pady=10, padx=7)
password_label.grid(column=0, row=3, padx=7)
website_label_entry.grid(column=1, row=1, ipady=12)
email_username_label_entry.grid(column=1, row=2, ipady=11)
password_label_entry.grid(column=1, row=3, ipady=12)
generate_password_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, pady=5)
delete_button.grid(column=2, row=2, pady=10, padx=5)
copy_password.grid(column=2, row=4, pady=5)

search_button.grid(column=2, row=1)
window.mainloop()

