---

# 🤝 ConvertHub Contribution Guide

Thank you for wanting to contribute to **ConvertHub**! 🎉
We want to create **the largest open-source conversion library**, and every contribution counts, no matter how big or small.

---

## 🛠 Types of contributions welcome

* Add **new conversions** (units, currencies, formats, etc.)
* Improve the **user interface**
* Optimize **performance**
* Fix **bugs**
* Improve **documentation**
* Add or improve **tests**

---

## 📋 Prerequisites

Before contributing, make sure you:

* Have **Python 3.10+** installed
* Have **pip** and **virtualenv** installed
* Know the basics of **Git** and **GitHub**
* Read this guide all the way through 😉

---

## 🚀 How to contribute

1. **Fork** the repository
   At the top right of the GitHub page, click **Fork** to create your own copy of the project.

2. **Clone** your fork

```bash
   git clone https://github.com/<your-username>/converthub.git
   cd converthub
   ```

3. **Create a new branch**

```bash
   git checkout -b feature/name-of-your-feature
   ```

4. **Create a virtual environment**

```bash
   python -m venv env
   source env/bin/activate  # Mac/Linux
   env\Scripts\activate     # Windows
   ```

5. **Install dependencies**

```bash
   pip install -r requirements.txt
   ```

6. **Configure the database**

```bash
   python manage.py migrate
   ```

7. **Launch the development server**

```bash
   python manage.py runserver
   ```

8. **Code your contribution**

   * Add your changes
   * Follow the existing code structure
   * Document any new features

9. **Test your changes**

```bash
   python manage.py test
   ```

10. **Commit** your changes

```bash
   git commit -m “Add: temperature conversion”
   ```

11. **Push** your branch

```bash
git push origin feature/name-of-your-feature
```

12. **Create a Pull Request (PR)**
Go to your fork on GitHub, click on **Compare & Pull Request** and clearly describe your changes.

---

## 🧾 Best practices

* Follow the project's coding style (**PEP8**)
* Give **clear names** to variables, functions, and files
* Comment on complex parts
* Always test before sending your PR
* Prefer **several small PRs** to one huge change

---

## 💬 Need help?

Open an **Issue** on GitHub with a clear title and a precise description.
We will be happy to answer you!

---

🚀 Thank you for helping to build **ConvertHub** — together, let's create **the ultimate conversion tool**! 🌍

---
