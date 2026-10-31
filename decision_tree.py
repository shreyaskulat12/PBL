
# Decision Tree Classifier using Iris Dataset

# Step 1: Import libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Step 2: Load Iris Dataset
iris = load_iris()

X = iris.data
y = iris.target

print("Feature names:", iris.feature_names)
print("Class names:", iris.target_names)
print("Dataset shape:", X.shape)

# Step 3: Split Training and Testing Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Step 4: Create Decision Tree Classifier
model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=3,
    random_state=42
)

# Step 5: Train the Model
model.fit(X_train, y_train)

# Step 6: Make Predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate Model
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy * 100, "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=iris.target_names
))

# Step 8: Display Decision Tree Rules
print("\nDecision Tree Rules:")

rules = export_text(
    model,
    feature_names=list(iris.feature_names)
)

print(rules)

# Step 9: Predict a New Flower
sample = [[5.0, 3.4, 1.5, 0.2]]

prediction = model.predict(sample)[0]

print("\nNew Flower Prediction:")
print(iris.target_names[prediction])
