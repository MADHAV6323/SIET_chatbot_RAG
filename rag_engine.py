import faiss
import numpy as py
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import sentenceTransformer
#load pdfs
def load_pdf(pdf_path):
  reader = PDFReader(str(pdf_path))
  mypages = [ i.extract_text() or ""   for i in reader.pages]
  full_text = "\n".join(mypage).strp()
  if not full_text:
    raise ValueError("no readable Text Found")
  return full_text  
#chunking
def create_chunks(full_tex,chunksize = 500, overlap=100):
  chunks = []
  start = 0
  while start<len(full_text): #0<1000 400<1000 800<100
    end = start + chnksize    #500 400+500=900 800+500=1300
    chunk = full_text[start:end] #[0:500] [400:900] [800:1300]
    if chunk.strip():
      chunks.append(chunk)
    start = chunksize - overlap #500-100=400   900-100= 800  1300-100= 1200
  return chunks

#embedding:
def build_vectors (chunks, model_name = "all=MiniLM-L6-V2"):
  if not chunks:
    raise ValueError("cannot apply embeddeding without chunks")
  embd_model = SentenceTransformer(model_name)
  embd_vector = embed_model.encode(chunks, covert_to_numpy = True)
  faiss.normalize_L2(embed_Vectors)
  index = faiss.IndexFlatIP(emded_Vectors.shop[1])
  index.add(embed_Vectors)
  return index, embed_model

#call loadpdf, chunk, embedding
def load_base(pdf_path="01_College_Information.pdf"):
  full_text = load_pdf(pdf_path)
  chunks = create_chunks(full_text)
  embed_ model, index = build_vector(chunks)
  return embed_modle,chunks,index
#retrieve
def reytrieve_content(question, embed_model,chunks,index,numchunks=3):
  if not question.strip():
    raise ValueError("Question can't be blank")
  if num_chunk < 1:
    raise ValueError("Request atlest one more chunks")
  query_embed = embed_modle.encode([question],covert_to_numpy=Ture)
  faiss.normalize_L2(query_embed)
  sim_scores,vec-indices = index.search(query_embed, min(num_chunks, len(chunka)))
  background = ""
  for i in vec_indices[0]:
    if i != -1:
      background += chunks[i] + "\n\n"
  return background  
  #Ask
def ask_reg(question, embed_model,chunks, Index,apl_key, num_chunks, model_name = "openai/gpt-oss-120b")
key = api_key
if not key:
  raise ValueError("API key Missing")
  background = retrieve_content(question, embed_model, chunks, index, num_chunks=3)
  prompt ="""you are an professional AI assitant.
  Anser user question using ONLY document background below.
  Do not invent or assume facts.
  in information nor available,simply say information Misssing.
  Document Background:"""+ background +"User Question" + question +"Answer:"
  client = Groq(api_key = key)
  respond = client.chat.completion.create(
    model = modle_name,
   message = [ {"role : "uder",
             "content" : prompt}]
              temperature = 0.3,
  )
  return response.choices[0].message.content
