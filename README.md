# Swiggy-s-Restaurant-Recommendation-System-using-Streamlit

## 📌 Overview

This project presents a personalized restaurant recommendation system inspired by Swiggy. It recommends restaurants based on user preferences like **city, cuisine, rating, rating_count, and cost** using clustering or similarity-based techniques. The final solution is presented through a user-friendly **Streamlit web application**.

---

## 🧠 Objective
The objective is to build a recommendation system based on restaurant data provided in a CSV file. 
- Clean and preprocess real-world restaurant data.
- Encode categorical variables using One-Hot Encoding and MultiLabel Binarizer.
- Apply K-Means clustering or Cosine Similarity for recommendations.
- Build a Streamlit app for interactive input and restaurant suggestions.

---

## 📁 File Structure

| Path                            | Description                                       |
|---------------------------------|---------------------------------------------------|
| `D:\APS\cleaned_data.csv`       | Cleaned dataset with relevant columns for display |
| `D:\APS\encoded_data.joblib`    | Encoded and numerical dataset for modeling        |
| `D:\APS\Swiggy.ipynb`           | Jupyter notebook containing full analysis         |
| `D:\APS\App.py`                 | Streamlit app that delivers recommendations       |

---

## 🧹 Data Cleaning

Performed in `Swiggy.ipynb`:

- Dropped duplicate rows based on name, city, and address.
- Handled missing values in `city`, `rating`,`rating_count`, `cost`, and `cuisine`.
- Exported clean output to `cleaned_data.csv`.

---

## ⚙️ Preprocessing

- **One-Hot Encoding** applied to `city`.
- **MultiLabel Binarizer** is used for `cuisine`.
- Numerical columns are used: `rating`, `rating_count`, and `cost`.
- Final encoded data saved using **Joblib** to `encoded_data.joblib`.

---

## 🤖 Recommendation Logic

Implemented in `Swiggy.ipynb`:

### 🔹 K-Means Clustering
- Clustered encoded restaurants.
- For user input, determined the nearest cluster and returned restaurants from it.

Recommendations are mapped back to the cleaned dataset (`cleaned_data.csv`) for display.

---

## 💻 Streamlit Application

Developed in `App.py`, the app provides:

- **Input Interface**:  
  - Dropdown: City  
  - Multi-select: Cuisines  
  - Sliders: Rating, Cost, Rating_count

- **Output**:  
  - Top N recommended restaurants with name, rating, cuisine, city, rating_count, and cost

### ▶️ To Run the App:
```bash
cd D:\APS
streamlit run App.py

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Your Name : Ashwini M
GitHub: https://github.com/ashwini98
