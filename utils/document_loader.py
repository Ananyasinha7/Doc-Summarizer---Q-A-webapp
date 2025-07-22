from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile, os, docx2txt, pdfplumber

def load_and_split(file):
    suffix=os.path.splitext(file.name)[1]
    file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.read())
        path=tmp.name
    
    if suffix==".pdf":
        loader = PyPDFLoader(path)
    elif suffix==".txt":
        loader=TextLoader(path)
    elif suffix==".docx":
        loader=UnstructuredWordDocumentLoader(path)
    else:
        raise ValueError("Unsupported file type: {}".format(suffix))
    
    docs=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100, 
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(docs)


def extract_preview(file, max_chars=1000):
    suffix=os.path.splitext(file.name)[1]
    file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.read())
        path=tmp.name
    
    text=""

    try:
        if suffix==".pdf":
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages[:2]:
                    text+=page.extract_text() or ""
        elif suffix==".txt":
            text=open(path, 'r', encoding='utf-8').read()
        return text.strip()[:max_chars]
    
    except Exception as e:
        return f"Error extracting preview: {e}"
    
    