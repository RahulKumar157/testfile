import streamlit as st

import pandas as pd
import base64
from pathlib import Path

# Custom CSS for styling
def local_css(style):
    with open(style) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        

local_css("style.css")


# Sidebar navigation menu at the top
st.sidebar.title("Smart File Preview")
pages = {
    "Home": "main",
    "Features": "features",
    "Upload": "upload",
    "Formats": "formats",
    "How It Works": "how_it_works",
    "Security": "security",
    "FAQ": "faq",
    "Contact": "contact"
}

# Create navigation buttons in the sidebar
for page_name, page_key in pages.items():
    if st.sidebar.button(page_name):
        st.session_state.page = page_key
        
# Check if a page is selected and display content (for demonstration, we'll show the current page)
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Upload"  # Default to "Upload" since it's the current functionality

if st.session_state.selected_page == "Upload":
    st.title(" Smart File Preview")
    st.subheader("Drag & Drop Files to Preview")

    # Create drag-and-drop area
    uploaded_file = st.file_uploader(
        label=" ",
        type=["csv", "xls", "xlsx", "html", "py", "txt"],
        accept_multiple_files=False,
        key="file_uploader"
    )

    # Preview section with fixed size
    if uploaded_file:
        st.markdown("### File Preview")
        file_type = uploaded_file.type.split('/')[-1]
        
        # Create scrollable container
        with st.container():
            st.markdown(f"**File Name:** {uploaded_file.name}")
            st.markdown(f"**File Type:** {file_type.upper()}")
            
            preview_box = st.empty()
            with preview_box.container():
                st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
                
                try:
                    if file_type in ["csv", "vnd.ms-excel", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                        df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
                        st.dataframe(df.head(10), height=300)
                    
                    elif file_type == "html":
                        html_content = uploaded_file.getvalue().decode("utf-8")
                        st.markdown(html_content, unsafe_allow_html=True)
                    
                    elif file_type in ["plain", "x-python"]:
                        code = uploaded_file.getvalue().decode("utf-8")
                        st.code(code, language='python' if file_type == 'x-python' else 'text')
                    
                    else:
                        st.warning("Preview not available for this file type")
                
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)
elif st.session_state.page == "features":
    st.title("Features")
    st.write("Here are the features of Smart File Preview...")
elif st.session_state.page == "upload":
    st.title("Upload")
    st.subheader("Upload History and File Preview")

    # Display upload history in a preview box
    st.markdown("### Upload History")
    with st.container():
        st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
        if st.session_state.upload_history:
            for file_name in st.session_state.upload_history:
                st.write(f"- {file_name}")
        else:
            st.write("No files have been uploaded yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Add drag-and-drop area for new uploads
    uploaded_file = st.file_uploader(
        label=" ",
        type=["csv", "xls", "xlsx", "html", "py", "txt"],
        accept_multiple_files=False,
        key="upload_uploader"
    )

    # Preview section for new uploads
    if uploaded_file:
        st.session_state.recent_file = uploaded_file  # Store the recent file
        st.session_state.upload_history.append(uploaded_file.name)  # Add file name to history
        st.markdown("### File Preview")
        file_type = uploaded_file.type.split('/')[-1]
        
        
        # Create scrollable container for preview
        with st.container():
            st.markdown(f"**File Name:** {uploaded_file.name}")
            st.markdown(f"**File Type:** {file_type.upper()}")
            
            preview_box = st.empty()
            with preview_box.container():
                st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
                
                try:
                    if file_type in ["csv", "vnd.ms-excel", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                        df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
                        st.dataframe(df.head(10), height=300)
                    
                    elif file_type == "html":
                        html_content = uploaded_file.getvalue().decode("utf-8")
                        st.markdown(html_content, unsafe_allow_html=True)
                    
                    elif file_type in ["plain", "x-python"]:
                        code = uploaded_file.getvalue().decode("utf-8")
                        st.code(code, language='python' if file_type == 'x-python' else 'text')
                    
                    else:
                        st.warning("Preview not available for this file type")
                
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.recent_file:  # Show recent file if no new upload
        st.markdown("### Recent File Preview")
        file_type = st.session_state.recent_file.type.split('/')[-1]
        
        with st.container():
            st.markdown(f"**File Name:** {st.session_state.recent_file.name}")
            st.markdown(f"**File Type:** {file_type.upper()}")
            
            preview_box = st.empty()
            with preview_box.container():
                st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
                
                try:
                    if file_type in ["csv", "vnd.ms-excel", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                        df = pd.read_csv(st.session_state.recent_file) if file_type == "csv" else pd.read_excel(st.session_state.recent_file)
                        st.dataframe(df.head(10), height=300)
                    
                    elif file_type == "html":
                        html_content = st.session_state.recent_file.getvalue().decode("utf-8")
                        st.markdown(html_content, unsafe_allow_html=True)
                    
                    elif file_type in ["plain", "x-python"]:
                        code = st.session_state.recent_file.getvalue().decode("utf-8")
                        st.code(code, language='python' if file_type == 'x-python' else 'text')
                    
                    else:
                        st.warning("Preview not available for this file type")
                
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "features":
    st.title("Features")
    st.write("Here are the features of Smart File Preview...")
elif st.session_state.page == "upload":
    st.title("Upload")
    st.subheader("Upload History and Recent File")

    # Display upload history in a preview box
    st.markdown("### Upload History")
    with st.container():
        st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
        if st.session_state.upload_history:
            for file_name in st.session_state.upload_history:
                st.write(f"- {file_name}")
        else:
            st.write("No files have been uploaded yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Add drag-and-drop area for new uploads on Upload page
    uploaded_file = st.file_uploader(
        label=" ",
        type=["csv", "xls", "xlsx", "html", "py", "txt"],
        accept_multiple_files=False,
        key="file_uploader_upload"
    )

    # Handle file upload and display recent file on Upload page
    if uploaded_file:
        st.session_state.recent_file = uploaded_file  # Store the recent file
        st.session_state.upload_history.append(uploaded_file.name)  # Add file name to history
        st.markdown("### New File Preview")
        file_type = uploaded_file.type.split('/')[-1]
        
        # Create scrollable container for preview
        with st.container():
            st.markdown(f"**File Name:** {uploaded_file.name}")
            st.markdown(f"**File Type:** {file_type.upper()}")
            
            preview_box = st.empty()
            with preview_box.container():
                st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
                
                try:
                    if file_type in ["csv", "vnd.ms-excel", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                        df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
                        st.dataframe(df.head(10), height=300)
                    
                    elif file_type == "html":
                        html_content = uploaded_file.getvalue().decode("utf-8")
                        st.markdown(html_content, unsafe_allow_html=True)
                    
                    elif file_type in ["plain", "x-python"]:
                        code = uploaded_file.getvalue().decode("utf-8")
                        st.code(code, language='python' if file_type == 'x-python' else 'text')
                    
                    else:
                        st.write("Preview not available for this file type")
                
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.recent_file:  # Show recent file if no new upload
        st.markdown("### Recent File Preview")
        file_type = st.session_state.recent_file.type.split('/')[-1]
        
        with st.container():
            st.markdown(f"**File Name:** {st.session_state.recent_file.name}")
            st.markdown(f"**File Type:** {file_type.upper()}")
            
            preview_box = st.empty()
            with preview_box.container():
                st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
                
                try:
                    if file_type in ["csv", "vnd.ms-excel", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                        df = pd.read_csv(st.session_state.recent_file) if file_type == "csv" else pd.read_excel(st.session_state.recent_file)
                        st.dataframe(df.head(10), height=300)
                    
                    elif file_type == "html":
                        html_content = st.session_state.recent_file.getvalue().decode("utf-8")
                        st.markdown(html_content, unsafe_allow_html=True)
                    
                    elif file_type in ["plain", "x-python"]:
                        code = st.session_state.recent_file.getvalue().decode("utf-8")
                        st.code(code, language='python' if file_type == 'x-python' else 'text')
                    
                    else:
                        st.warning("Preview not available for this file type")
                
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "formats":
    st.title("Formats")
    st.write("Supported file formats: CSV, XLS, XLSX, HTML, PY, TXT...")
elif st.session_state.page == "how_it_works":
    st.title("How It Works")
    st.write("Learn how Smart File Preview works...")
elif st.session_state.page == "security":
    st.title("Security")
    st.write("Details about security and privacy...")
elif st.session_state.page == "faq":
    st.title("FAQ")
    st.write("Frequently Asked Questions...")
elif st.session_state.page == "contact":
    st.title("Contact")
    st.write("Contact us for support...")
    # Add footer (visible on all pages)
st.markdown("""
    <footer style="
        background-color: #1e1e2f;
        color: #ffffff;
        text-align: center;
        padding: 1rem;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        box-shadow: 0 -2px 4px rgba(0, 0,0, 0.1);
    ">
        © 2025 Smart File Preview. All rights reserved. | <a href="#" style="color: #4a90e2; text-decoration: none;">Privacy Policy</a> | <a href="#" style="color: #4a90e2; text-decoration: none;">Contact Us</a>
    </footer>
""", unsafe_allow_html=True)