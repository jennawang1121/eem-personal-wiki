from datetime import datetime, timezone
from wiki import ROOT,LocalGemma,ask,chat_turn,save_record,read_json,write_json
model=LocalGemma(); stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
latest=read_json(ROOT/'evidence/latest-evaluation.json')
for name,record in [('ask-chinese',ask('根據筆記，LCOE 有哪些限制？',model)),('chat-notes',chat_turn('/notes What are the limitations of LCOE in my notes?',[],model))]:
    path=save_record(record,name=stamp+'-'+name)
    latest['records']=[str(path.relative_to(ROOT)) if p.endswith('-'+name+'.md') else p for p in latest['records']]
    print(name,record['answer'],flush=True)
write_json(ROOT/'evidence/latest-evaluation.json',latest)
