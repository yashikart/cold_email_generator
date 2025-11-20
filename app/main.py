import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner("Loading and processing..."):
            try:
                # Step 1: Load webpage
                st.info("📥 Loading webpage...")
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                
                # Step 2: Load portfolio
                st.info("📚 Loading portfolio...")
                portfolio.load_portfolio()
                
                # Step 3: Extract jobs
                st.info("🔍 Extracting job information...")
                jobs = llm.extract_jobs(data)
                
                # Step 4: Generate emails
                st.info("✍️ Generating emails...")
                for i, job in enumerate(jobs, 1):
                    with st.expander(f"Job {i}: {job.get('role', 'Unknown Role')}", expanded=True):
                        st.json(job)
                        skills = job.get('skills', [])
                        if isinstance(skills, str):
                            skills = [skills]
                        
                        links = portfolio.query_links(skills)
                        st.info(f"📎 Relevant portfolio links: {links}")
                        
                        email = llm.write_mail(job, links)
                        st.markdown("### Generated Email:")
                        st.markdown(email)
                        st.code(email, language=None)
            except Exception as e:
                st.error(f"An Error Occurred: {e}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


