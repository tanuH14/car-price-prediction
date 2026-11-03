
import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# Load trained model
@st.cache_resource
def load_model():
    return joblib.load("car_price_model.joblib")

bundle = load_model()

model = bundle["model"]
feature_columns = bundle["feature_columns"]
categorical_columns = bundle["categorical_columns"]
numerical_columns = bundle["numerical_columns"]
categorical_options = bundle["categorical_options"]
numeric_defaults = bundle["numeric_defaults"]

# Application heading
st.title("🚗 Used Car Price Prediction")
st.write(
    "Predict the estimated selling price of a used car "
    "using Machine Learning."
)

st.divider()

st.subheader("Enter Your Car Details")

input_values = {}

# Create two-column input layout
left_col, right_col = st.columns(2)

for index, column in enumerate(feature_columns):

    current_col = left_col if index % 2 == 0 else right_col

    with current_col:

        if column in categorical_columns:

            options = categorical_options[column]

            if options:
                input_values[column] = st.selectbox(
                    column.replace("_", " ").title(),
                    options=options
                )

            else:
                input_values[column] = st.text_input(
                    column.replace("_", " ").title()
                )

        elif column in numerical_columns:

            default_value = numeric_defaults[column]

            input_values[column] = st.number_input(
                column.replace("_", " ").title(),
                value=float(default_value),
                step=1.0
            )

# Prediction button
st.divider()

if st.button("Predict Car Price", type="primary", use_container_width=True):

    input_df = pd.DataFrame(
        [input_values],
        columns=feature_columns
    )

    prediction = model.predict(input_df)[0]

    st.success("Prediction completed successfully!")

    st.subheader("Estimated Car Price")

    st.metric(
        label="Predicted Selling Price",
        value=f"{prediction:,.2f}"
    )

    st.caption(
        "The prediction is an estimate based on your trained "
        "machine learning model. The displayed value uses "
        "the same price units as the training dataset."
    )

st.divider()

st.caption(
    "Powered by Hist Gradient Boosting | "
    "Machine Learning Car Price Prediction Project"
)
