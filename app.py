from fastapi import Body, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, constr
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline,AutoModelForQuestionAnswering
# import google_trans_parrot as gp
from parrot import Parrot
import googletrans

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")

def language_translate(source_sentence,target_language = "english"):
    translator = googletrans.Translator(service_urls=['translate.google.com', 'translate.google.co.kr',])
    # 先將想要的目標語言(target_language)轉為英文，以便等等可以用dest指定轉換到的語言
    language_dest = translator.translate(text = target_language,dest = 'english').text.lower()
    # 如果是要轉成中文，要變成dest看得懂的格式 
    # 將source_sentence丟入，再指定要轉換到的語言(dest)
    output_sentence = translator.translate(text = source_sentence,dest = language_dest).text
    return output_sentence

def simple_parrot(input_sentence):
    print("input_sentence",input_sentence)
    translated_paragraph = language_translate(input_sentence,'english')
    para_phrases = parrot.augment(input_phrase=input_sentence,
                        use_gpu = False,
                        diversity_ranker="levenshtein",
                        #do_diverse = False, 
                        do_diverse = True, 
                        max_return_phrases = 10, 
                        #truncation = True,
                        max_length=512, 
                        adequacy_threshold = 0.30,  
                        fluency_threshold = 0.30)
    # sel_para = para_phrases[len(para_phrases)-1][0]
    sel_para = para_phrases[0][0]
    ch_translated_paragraph = language_translate (sel_para, "chinese (traditional)")
    return ch_translated_paragraph

class NERRequest(BaseModel):
    #sentance: constr(max_length=512)
    sentance: str
class QARequest(BaseModel):
    maintext: constr(max_length=512)
    subtext: constr(max_length=512)
class ParaRequest(BaseModel):
    #sentance: constr(max_length=512)
    sentance: str
class NERItem(BaseModel):
    entity: str
    score: float
    index: int
    word: str
    start: int
    end: int


app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_short_description }}",
    version="{{ cookiecutter.version }}",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

#text-generate(QA,QG,Summarization .etc)
generation_tokenizer=AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
generation_model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
generation_pipeline=pipeline("question-answering", model=generation_model, tokenizer=generation_tokenizer)

@app.get("/")
async def root():
    return RedirectResponse("docs")


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    return templates.TemplateResponse(f"{page_name}.html", {"request": request})


#
# NER
#


@app.post("/ner")
async def ner(
    ner_request: NERRequest = Body(
        None,
        examples={
            "Example 1": {
                "value": {"sentance": "My name is Wolfgang and I live in Berlin"}
            },
            "Example 2": {
                "value": {"sentance": "My name is Sarah and I live in London"}
            },
            "Example 3": {
                "value": {
                    "sentance": "My name is Clara and I live in Berkeley, California."
                }
            },
        },
    )
):
    results = ner_pipeline(ner_request.sentance)
    validated = [NERItem(**item) for item in results]
    return validated

@app.post("/qa")
async def qa(
    qa_request: QARequest = Body(
        None,
        
    )
):
    print(qa_request)
    model_input={
        "question":qa_request.maintext,
        "context":qa_request.subtext
    }
    results = generation_pipeline(model_input)
    # validated = [NERItem(**item) for item in results]
    return results

@app.post("/para")
async def para(
    para_request: ParaRequest = Body(
        None,
    )
):
    print("para_request",para_request)
    # model_input={
    #     "sentence":para_request.sentance
    # }

    # results = generation_pipeline(model_input)
    # sel_para = simple_parrot(para_request.sentance)
    
    para_phrases = parrot.augment(input_phrase=para_request.sentance,
                            use_gpu = False,
                            diversity_ranker="levenshtein",
                            # do_diverse = False, 
                            do_diverse = True, 
                            max_return_phrases = 10, 
                            #truncation = True,
                            max_length=512, 
                            adequacy_threshold = 0.30,  
                            fluency_threshold = 0.30)
    # validated = [NERItem(**item) for item in results]
    print(para_phrases)
    # sel_para = para_phrases[len(para_phrases)-1][0]
    sel_para = para_phrases[0][0]
    print("sel_para",sel_para)
    return sel_para