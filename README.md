# 🌍 ConvertHub

**The open-source tool for converting absolutely everything** — units, currencies, file formats, number bases, languages... and much more.
Our goal: to create **the world's largest conversion library**, powered by the community.

---

## 🚀 Features

* 🔄 **Units**: length, weight, temperature, speed...
* 💱 **Currencies**: real-time conversion with API exchange rates
* 📂 **Formats**: images, audio, video, documents, text
* 🧮 **Number bases**: binary, octal, hexadecimal, decimal
* 🌐 **Languages**: quick and easy translation
* 📅 **Other**: time zones, calendars, date formats

> **Anyone can contribute** — add new conversions, improve the interface, or optimize the code.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/converthub.git
cd converthub
```

---

### 2. Django backend

#### a) Create a virtual environment

```bash
python -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows
```

#### b) Install dependencies

```bash
pip install -r requirements.txt
```

#### c) Configure the database

```bash
python manage.py migrate
```

#### d) Start the Django server

```bash
python manage.py runserver
```

> The backend runs by default on `http://127.0.0.1:8000/`

---

### 3. React frontend

#### a) Install dependencies

```bash
cd frontend
npm install
```

#### b) Launch the frontend

```bash
npm start
```

> The frontend runs by default on `http://localhost:3000/` and communicates with the backend via the Django API.

---

## 🤝 Contribute

1. **Fork** the project
2. **Create** your branch (`git checkout -b feature/my-conversion`)
3. **Commit** your changes (`git commit -m ‘Add temperature conversion’`)
4. **Push** to your branch (`git push origin feature/my-conversion`)
5. **Open a Pull Request**

> See the [`CONTRIBUTING.md`](CONTRIBUTING.md) file for more details.

---

## 📜 License

This project is licensed under **MIT** — feel free to use, modify, and share it.

---

## 🌟 Support the project

* ⭐ **Star** the repo
* 📢 Share it on your networks
* 💡 Suggest your ideas in the Issues

---

💬 *“Alone we go faster, together we go further.”* — What if we created **the ultimate conversion tool**? 🚀

---
