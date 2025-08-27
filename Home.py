import streamlit as st
import pandas as pd
import seaborn as sns
import os
import base64

# --- Page Config (MUST be the first Streamlit command) ---
st.set_page_config(page_title="Automated Data Analyzer", page_icon="📊", layout="wide")

# --- Custom Background (Image + Overlay) ---
background_image = "E:/MSC_MU/SEM-2/Main_Project/Dark.png"  # <-- change to your image path

if os.path.exists(background_image):
    with open(background_image, "rb") as img_file:
        img_bytes = img_file.read()
    img_base64 = base64.b64encode(img_bytes).decode()

    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: 
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),  /* Dark overlay */
            url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #f5f5f5;  /* Global light text */
    }}
    
    /* Header */
    [data-testid="stHeader"] {{
        background: rgba(32, 201, 151, 0.8);  /* Teal translucent */
        color: white;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: rgba(20, 20, 35, 0.9);
        color: #f5f5f5;
    }}
    [data-testid="stSidebar"] * {{
        color: #f5f5f5 !important;
    }}

    /* Titles & text */
    h1, h2, h3, h4, h5, h6 {{
        color: #20c997;  /* Bright teal */
        text-shadow: 1px 1px 4px rgba(0,0,0,0.7);
    }}
    p, label, span {{
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
    }}

    /* Buttons */
    .stButton > button {{
        background-color: #20c997;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 20px;
        border: none;
        transition: 0.3s;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    }}
    .stButton > button:hover {{
        background-color: #ff6f61;
        transform: scale(1.05);
    }}

    /* DataFrame Styling */
    .stDataFrame {{
        background: rgba(20,20,40,0.85);
        border-radius: 8px;
        padding: 10px;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
else:
    st.error("Background image not found. Please check the path.")

# --- Initialize Session State ---
if 'df' not in st.session_state:
    st.session_state['df'] = None

# --- Data Loader Function ---
def load_data(uploaded_file):
    """Loads data from CSV or Excel file."""
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    return df

# --- Title & Description ---
st.markdown(
    """
    <div style="text-align: center;">
        <h1>✨ Automated Data Analyzer & Visualization System ✨</h1>
        <p style='font-size:18px; color:#f0f0f0;'>
            Upload your dataset, explore insights, and generate beautiful graphs effortlessly 🚀
        </p>
    </div>
    """, unsafe_allow_html=True
)
st.info("📌 Use the sidebar to navigate between pages.")

# --- Upload Section ---
st.title("📊 Data Upload & Overview")

uploaded_file = st.file_uploader("📂 Upload your CSV or Excel file", type=["csv", "xlsx"])

st.markdown("---")
st.subheader("Or load an example dataset:")
example_dataset = st.selectbox(
    "Choose an example dataset:",
    ["None", "Iris", "Tips", "Titanic"],
    key="example_data_selector"
)

# --- Handle Data Loading ---
df_loaded = None
if uploaded_file is not None:
    try:
        df_loaded = load_data(uploaded_file)
        st.session_state['df'] = df_loaded
        st.success("🎉 Data uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading uploaded file: {e}")
elif example_dataset != "None":
    with st.spinner(f"Loading {example_dataset} dataset..."):
        try:
            if example_dataset == "Iris":
                df_loaded = sns.load_dataset("iris")
            elif example_dataset == "Tips":
                df_loaded = sns.load_dataset("tips")
            elif example_dataset == "Titanic":
                df_loaded = sns.load_dataset("titanic")
            st.session_state['df'] = df_loaded
            st.success(f"🎉 {example_dataset} dataset loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading example dataset: {e}")

# --- Data Preview & Stats ---
if 'df' in st.session_state and st.session_state['df'] is not None:
    df = st.session_state['df']
    st.subheader("🔍 Preview of Loaded Data")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("📑 Basic Data Statistics")
    st.dataframe(df.describe(include="all"), use_container_width=True)
else:
    st.warning("⚠ Please upload a dataset or select an example dataset to get started.")

# --- Footer ---
st.markdown(
    "<hr><center>🚀 Developed by <b style='color:#20c997;'>Kishor Goraniya</b> | BCA Data Science Project</center>",
    unsafe_allow_html=True
)
