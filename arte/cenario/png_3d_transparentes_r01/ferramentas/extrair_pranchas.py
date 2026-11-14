from PIL import Image,ImageDraw,ImageFont
import numpy as np
from scipy import ndimage as ndi
from pathlib import Path
import json,csv,hashlib,zipfile,html,re
ROOT=Path('/workspace/scratch/ed59ed9c2eda'); OUT=ROOT/'Fazenda_Capricho_PNG';OUT.mkdir(exist_ok=True)
# Label top coordinates were checked against the source sheets. Row-major order follows the PDF.
CONFIG=[
('01_quarto_meninas','Beliche rosa sobre fundo branco.png',[328,614,901,1179,1450],50,
'beliche castelo_frente castelo_interior escada escorregador janela mesinha objeto_almofada objeto_biscoito objeto_escova objeto_pelucia parede piso porta porta_castelo_aberta porta_castelo_fechada pote_biscoitos quadro_ferradura tapete varal_coracoes'),
('02_sala','Catálogo 3D da sala Fazenda Capricho.png',[279,536,794,1022,1277,1485,1725],50,
'abajur_aceso abajur_apagado almofada_lilas almofada_rosa cesto_brinquedos estante fogo_alto fogo_baixo fundo lareira livro_azul livro_rosa mesa_centro placa_casa placa_coracao placa_flor placa_panela plantinha porta_aberta porta_fechada porta_retrato previa sofa tapete vaso_flores'),
('03_cozinha','Catálogo 3D da Cozinha Fazenda Capricho.png',[279,553,788,1039,1255,1446,1723],50,
'banana cadeira copo_leite fogao fogao_vapor fundo geladeira_aberta geladeira_fechada maca mesa pia placa_casa porta_aberta porta_fechada prato_limpo prato_sujo previa sanduiche tigela_cao_cheia tigela_cao_vazia tigela_gato_cheia tigela_gato_vazia tigela_lumi_cheia tigela_lumi_vazia vaso_flores xicara'),
('04_sede','Catálogo 3D de brinquedos Fazenda Capricho.png',[313,594,890,1153,1452],48,
'banco_varanda bola cadeira_deck fundo lanterna_acesa lanterna_apagada luzinhas_acesas luzinhas_apagadas mesa_deck porta_frente_aberta porta_frente_fechada previa rede regador_cheio regador_vazio vaso_1 vaso_2 vaso_3'),
('05_entrada','Catálogo 3D da Entrada Fazenda Capricho.png',[347,661,961,1302],45,
'arco_portal banco cartinha correio_aberto correio_fechado flor floreira floreira_colhida fundo lanterna_acesa lanterna_apagada moinho_helice moinho_torre portao_aberto portao_fechado previa'),
('06_quarto_carol','Catálogo 3D do Quarto da Carol.png',[286,546,836,1107,1378,1598],48,
'abajur_aceso abajur_apagado banquinho cama cobertor_coberto cobertor_dobrado criado_mudo escova_cabelo fundo guarda_roupa_aberto guarda_roupa_fechado penteadeira penteadeira_brilho placa_casa planta porta_aberta porta_fechada porta_retrato_coracao porta_retrato_paisagem previa tapete travesseiro'),
('07_estabulo','Catálogo 3D do Estábulo Fazenda Capricho.png',[242,470,721,960,1189,1374,1585,1817,1965],44,
'arvore balde_agua balde_vazio banco_tronco cocho_cenouras cocho_feno cocho_vazio ducha_desligada ducha_ligada espuma_1 espuma_2 espuma_3 fardo feno ferradura fundo laguinho_ondas laguinho_parado lanterna_acesa lanterna_apagada margarida meia_porta_aberta meia_porta_fechada moita_colhida moita_flores pente piso_banho porteira_aberta porteira_fechada previa suporte_manta toalha toalha_gancho'),
('08_plantacao','Catálogo 3D da Fazenda Capricho.png',[132,237,353,480,603,702,810,914,1004,1132,1246,1337,1446,1537,1633,1717,1790,1881,1957,2033,2094,2157],29,
'abelha_aberta abelha_fechada abobora_gigante abobora_media abobora_pequena alface_1 alface_2 alface_3 alface_4 arbusto_coracoes banana bananeira_com bananeira_sem banca bica borboleta_aberta borboleta_fechada buque cacho_banana cadeado canteiro_colhido canteiro_flores carrinho cenoura_1 cenoura_2 cenoura_3 cenoura_4 cesta_cheia cesta_vazia colheita_alface colheita_cenoura colheita_tomate contador covinha covinha_broto enxada escadinha espantalho estrelinha ferradurinha flor_arco_iris_amarela flor_arco_iris_azul flor_arco_iris_lilas flor_arco_iris_rosa flor_coracao flor_margarida flor_tulipa frutinhas_magicas_com frutinhas_magicas_sem fundo girassol_cabeca girassol_caule laranja laranjeira_com laranjeira_sem maca macieira_com_macas macieira_sem_macas matinho minhoca morango morango_0 morango_1 morango_2 morango_3 morango_4 nuvem_chovendo nuvem_parada previa quadro_pedidos regador_cheio regador_vazio semente_magica sementes_abobora sementes_alface sementes_cenoura sementes_girassol sementes_morango sementes_tomate terra_dura terra_fechada terra_fofa tomate_1 tomate_2 tomate_3 tomate_4'),
('09_pet_care','Catálogo 3D de cuidados para pets.png',[250,513,778,1038,1224,1436,1703],48,
'banheira_agua banheira_espuma banheira_vazia biscoito bolha bolinha cercadinho chuveirinho_desligado chuveirinho_ligado fundo gancho_toalha osso peixinho placa_pata prateleira previa tigela_agua_cheia tigela_agua_vazia tigela_cao_cheia tigela_cao_vazia tigela_gato_cheia tigela_gato_vazia toalha varinha_pena vaso_flores xampu'),
('10_casa_arvore','Catálogo 3D da Casa na Árvore.png',[226,414,627,840,1057,1238,1403,1594,1803,1987,2135],31,
'arvore_casinha balanco_assento balanco_estrutura bau_aberto bau_fechado bola brilho bule cacho_colhido cacho_com cadeirinha cama cesto_cheio cesto_vazio cozinha_desligada cozinha_ligada escada_corda escada_madeira escorregador_arco_iris escorregador_rosa frutinha fundo_dentro fundo_patio grade_varanda mesa_piquenique mesinha_cha panelinha passarinho_pousado passarinho_voando placa_cabana placa_casa porta_aberta porta_dentro_aberta porta_dentro_fechada porta_fechada previa_dentro previa_fora tapete unicornio ursinho_heroi xicara_cha xicara_vazia'),
('11_cabana','Catálogo 3D da Cabana Fazenda Capricho.png',[364,693,992,1264],43,
'binoculo cabana_aberta cabana_fechada fogueira fogueira_brilho fundo lanterna_desligada lanterna_ligada livro_aberto livro_fechado passarinho previa saco_dormir tronco_banco'),
('12_casinha','Catálogo 3D da Casinha Fazenda Capricho.png',[312,602,885,1163,1453],47,
'balcao cadeirinha caixa_registradora caixa_registradora_plim casinha casinha_interior coracao_batendo estetoscopio fundo maleta_aberta maleta_fechada placa_cesta placa_pata potinho_amarelo potinho_lilas potinho_rosa prateleira previa toldo_aberto toldo_fechado'),
('13_placas','Catálogo 3D de Plaquinhas de Caminho.png',[355,678,989,1301],46,
'seta_arvore_d seta_arvore_e seta_cabana_d seta_cabana_e seta_casa_d seta_casa_e seta_cenoura_d seta_cenoura_e seta_cesta_d seta_cesta_e seta_ferradura_d seta_ferradura_e seta_pata_d seta_pata_e seta_portao_d seta_portao_e'),
('14_mapa_botoes','Mapas e botões 3D da Fazenda Capricho.png',[342,640,941,1255],50,
'aqui botao_fechar botao_mapa cabana casa_arvore casa_arvore_dentro casinha cozinha entrada estabulo pet_care plantacao quarto quarto_carol sala sede')]

# Geometry and state warnings from direct comparison with the existing catalog.
WARNINGS={
'01_quarto_meninas':{'beliche':'A prancha mostra apenas uma plataforma; conferir projeto do beliche.','porta_castelo_aberta':'A arte parece uma porta fechada vista em perspectiva; redesenhar estado aberto.'},
'07_estabulo':{'cocho_cenouras':'O cocho contém brotos, sem cenouras claramente desenhadas.','meia_porta_aberta':'A abertura foi representada como painel estreito; validar montagem.','porteira_aberta':'Os dois postes são partes do mesmo arquivo, preservados juntos.'},
'08_plantacao':{'bananeira_com':'A bananeira está jovem e sem cacho visível.','canteiro_colhido':'A arte contém plantas; não corresponde ao estado colhido.','cenoura_1':'A arte contém cobertura tipo estufa; difere da fase 1 do PDF.','cenoura_3':'As folhas/formas não correspondem claramente a cenouras.','nuvem_chovendo':'Não há gotas visíveis; regenerar estado chovendo.','matinho':'A arte é uma flor roxa, diferente do matinho do PDF.','flor_coracao':'As pétalas não têm o formato de coração do PDF.','flor_arco_iris_amarela':'A flor não preserva o miolo arco-íris do PDF.','flor_arco_iris_azul':'A flor não preserva o miolo arco-íris do PDF.','flor_arco_iris_lilas':'A flor não preserva o miolo arco-íris do PDF.','flor_arco_iris_rosa':'A flor não preserva o miolo arco-íris do PDF.'},
'09_pet_care':{'banheira_vazia':'A arte ainda mostra uma superfície interna branca; conferir estado vazio.','tigela_agua_vazia':'A arte mantém pequenos detalhes internos; conferir vazio.'},
'10_casa_arvore':{'cozinha_ligada':'Conferir diferença visual para o estado desligado.','cacho_colhido':'As formas na prancha não deixam o estado colhido claro.'}}
# Plantacao image generation inserted a spurious extra seed packet before the expected packet sequence.
# It has 86 slots but 87 drawn items: row 19 has 4, row 20 has 4; mapping is handled explicitly below.

records=[]; diagnostics=[]
# Keep all 380 PDF identities; the extra packet is preserved separately after extraction.
# Derive label baselines per column, since generated rows are not perfectly level.
def label_bounds(filename, centers, ys, width):
 words=json.loads((ROOT/'work'/(Path(filename).stem+'.json')).read_text())
 ans=[]
 for y in ys:
  row=[]
  for col in range(4):
   q=[q for q in words if len(q['t'])>=3 and q['c']>25 and q['h']<25 and abs(q['y']-y)<25 and int(np.argmin(abs(centers-(q['x']+q['w']/2))))==col]
   # OCR text in the actual label band; fallback where full-image OCR misses a label.
   if q:
    best=min(q,key=lambda q:abs(q['y']-y));near=[q for q in q if abs(q['y']-best['y'])<8]
    row.append((int(min(q['y'] for q in near)),int(max(q['y']+q['h'] for q in near))))
   else: row.append((y,y+(12 if width<800 else 20)))
  ans.append(row)
 return ans
for scenario,filename,ys,top,names_str in CONFIG:
 names=names_str.split();im=Image.open(ROOT/'sources'/filename).convert('RGB');a=np.array(im)
 if scenario=='08_plantacao':centers=np.array([165,295,430,560])
 else:centers=np.array([(i+.5)*im.width/4 for i in range(4)])
 rowpad=14 if scenario=='08_plantacao' else (21 if im.width<800 else 27)
 bounds=label_bounds(filename,centers,ys,im.width)
 if scenario=='08_plantacao':
  bounds[17][1]=(1893,1901)
  bounds[15][0]=(1722,1732)
  bounds[15][1]=(1722,1732)
  bounds[15][2]=(1722,1732)
  bounds[15][3]=(1722,1732)
 edges=[0]+[int((centers[i]+centers[i+1])/2) for i in range(3)]+[im.width]
 for row,y in enumerate(ys):
  starts=[top]*4 if row==0 else [b[1]+5 for b in bounds[row-1]]
  ends=[b[0]-4 for b in bounds[row]]
  start=min(starts);end=max(ends)
  rgb=a[start:end].copy()
  for c in range(4):
   rgb[:max(0,starts[c]-start),edges[c]:edges[c+1]]=255
   rgb[max(0,ends[c]-start):,edges[c]:edges[c+1]]=255
  v=rgb.astype(np.int16)
  # Near-white connected to the exterior is background; enclosed whites remain intact.
  candidate=(v.min(2)>=241)&((v.max(2)-v.min(2))<=22)
  seed=np.zeros(candidate.shape,bool);seed[0]=candidate[0];seed[-1]=candidate[-1];seed[:,0]|=candidate[:,0];seed[:,-1]|=candidate[:,-1]
  bg=ndi.binary_propagation(seed,mask=candidate)
  fg=~bg
  lab,n=ndi.label(fg)
  comps=ndi.find_objects(lab);owners=np.full(n+1,-1)
  for k,sl in enumerate(comps,1):
   if sl is None:continue
   area=np.sum(lab[sl]==k)
   if area<7:continue
   # Drop OCR-size dark remnants without deleting colored stars, drops or dots.
   pixels=rgb[sl][lab[sl]==k]
   if area<150 and sl[0].stop-sl[0].start<18 and pixels.max(1).mean()<180:continue
   xx=np.nonzero(lab[sl]==k)[1]+sl[1].start
   owners[k]=int(np.argmin(abs(centers-np.mean(xx))))
  for col in range(4):
   idx=row*4+col
   if idx>=len(names):continue
   name=names[idx];mask=owners[lab]==col
   if not mask.any():raise RuntimeError((scenario,name,'EMPTY'))
   # Maintain antialiasing on the outer 1px contour, decontaminating white where alpha is fractional.
   boundary=mask & ndi.binary_dilation(bg,iterations=1)
   alpha=np.where(mask,255,0).astype(np.uint8)
   strength=np.clip((255-v.min(2))/20.,0,1)
   alpha[boundary]=(strength[boundary]*255).astype(np.uint8)
   ys0,xs0=np.nonzero(alpha>0);x0,x1=xs0.min(),xs0.max()+1;y0,y1=ys0.min(),ys0.max()+1
   rgba=np.dstack([rgb,alpha])[y0:y1,x0:x1].copy()
   aa=rgba[:,:,3].astype(float)/255
   frac=(aa>0)&(aa<1)
   for c in range(3):
    channel=rgba[:,:,c].astype(float)
    channel[frac]=np.clip((channel[frac]-255*(1-aa[frac]))/aa[frac],0,255)
    rgba[:,:,c]=channel.astype(np.uint8)
   # Interior openings in handles / structural frames must also be transparent.
   open_shapes=('escada','cadeira','cadeirinha','balanco_estrutura','lanterna','regador','cesta_vazia','cesto_vazio','balde','placa_','seta_')
   if any(name.startswith(z) for z in open_shapes):
    rv=rgba[:,:,:3].astype(int);holes=(rv.min(2)>=245)&((rv.max(2)-rv.min(2))<15)
    rgba[holes,3]=0
   rgba[rgba[:,:,3]==0,:3]=0
   cut=Image.fromarray(rgba,'RGBA');canvas=Image.new('RGBA',(cut.width+16,cut.height+16));canvas.paste(cut,(8,8))
   kind='previas' if name.startswith('previa') else ('fundos' if name.startswith('fundo') or name in ['parede','piso'] else ('interface' if scenario in ['13_placas','14_mapa_botoes'] else 'objetos'))
   path=OUT/scenario/kind/(name+'.png');path.parent.mkdir(parents=True,exist_ok=True);canvas.save(path,optimize=True)
   rec=dict(id=scenario+'/'+name,cenario=scenario,nome=name,tipo=kind,arquivo=str(path.relative_to(OUT)),largura=canvas.width,altura=canvas.height,origem=filename,recorte_origem=[int(x0),int(start+y0),int(x1),int(start+y1)],pivo=[.5,1],resolucao_baixa=min(cut.size)<64,revisao=WARNINGS.get(scenario,{}).get(name,''))
   records.append(rec)
   diagnostics.append((scenario,name,canvas.copy()))
 print(scenario,len(names),flush=True)
# Pair/group canvas dimensions and bottom-center placement without scaling source art.
pairs=[['porta_aberta','porta_fechada'],['porta_castelo_aberta','porta_castelo_fechada'],['abajur_aceso','abajur_apagado'],['lanterna_acesa','lanterna_apagada'],['luzinhas_acesas','luzinhas_apagadas'],['porta_frente_aberta','porta_frente_fechada'],['regador_cheio','regador_vazio'],['correio_aberto','correio_fechado'],['portao_aberto','portao_fechado'],['guarda_roupa_aberto','guarda_roupa_fechado'],['ducha_ligada','ducha_desligada'],['balde_agua','balde_vazio'],['laguinho_ondas','laguinho_parado'],['meia_porta_aberta','meia_porta_fechada'],['porteira_aberta','porteira_fechada'],['banheira_agua','banheira_espuma','banheira_vazia'],['chuveirinho_ligado','chuveirinho_desligado'],['tigela_agua_cheia','tigela_agua_vazia'],['tigela_cao_cheia','tigela_cao_vazia'],['tigela_gato_cheia','tigela_gato_vazia'],['tigela_lumi_cheia','tigela_lumi_vazia'],['bau_aberto','bau_fechado'],['cesto_cheio','cesto_vazio'],['cabana_aberta','cabana_fechada'],['lanterna_desligada','lanterna_ligada'],['livro_aberto','livro_fechado'],['maleta_aberta','maleta_fechada']]
for sc,*_ in CONFIG:
 for group in pairs:
  found=[r for r in records if r['cenario']==sc and r['nome'] in group]
  if len(found)<2:continue
  w=max(r['largura'] for r in found);h=max(r['altura'] for r in found)
  for r in found:
   path=OUT/r['arquivo'];orig=Image.open(path);can=Image.new('RGBA',(w,h));can.paste(orig,((w-orig.width)//2,h-orig.height));can.save(path,optimize=True)
   r.update(largura=w,altura=h,grupo_estados='/'.join(group),pivo=[.5,1])
# Correct generated seed-packet ordering to match the actual depicted species.
plant=[r for r in records if r['cenario']=='08_plantacao']
packet_names={73:'quadro_sementes_extra',74:'sementes_abobora',75:'sementes_alface',76:'sementes_cenoura',77:'sementes_girassol',78:'sementes_morango',79:'sementes_tomate'}
staged=[]
for idx,newname in packet_names.items():
 r=plant[idx];old=OUT/r['arquivo'];staged.append((r,newname,old.read_bytes()));old.unlink()
for r,newname,data in staged:
 path=OUT/r['cenario']/r['tipo']/(newname+'.png');path.write_bytes(data)
 r.update(id=r['cenario']+'/'+newname,nome=newname,arquivo=str(path.relative_to(OUT)))
 if newname=='quadro_sementes_extra':r['revisao']='Item extra inventado na prancha, fora dos 380 IDs do PDF.'
# Add missing compacted soil sprite, generated independently at higher resolution.
soil_path=ROOT/'generated_images/exec-0f7e4db7-a2f2-40c1-a4eb-77229c24364a.png'
cloud_path=ROOT/'generated_images/exec-a0942973-0ef5-47ef-9799-1abf88b88386.png'
def trim_alpha(img):
 ar=np.array(img);lab,n=ndi.label(ar[:,:,3]>16);sizes=np.bincount(lab.ravel());keep=sizes>100;keep[0]=False
 support=ndi.binary_dilation(keep[lab],iterations=2);ar[~support,3]=0
 b=Image.fromarray(ar,'RGBA');box=b.getbbox();b=b.crop(box);b.thumbnail((384,384),Image.Resampling.LANCZOS)
 return b
soil=trim_alpha(Image.open(soil_path).convert('RGBA'))
soil_can=Image.new('RGBA',(soil.width+16,soil.height+16));soil_can.paste(soil,(8,8));path=OUT/'08_plantacao/objetos/terra_dura.png';soil_can.save(path)
records.append(dict(id='08_plantacao/terra_dura',cenario='08_plantacao',nome='terra_dura',tipo='objetos',arquivo=str(path.relative_to(OUT)),largura=soil_can.width,altura=soil_can.height,origem=soil_path.name,recorte_origem=None,pivo=[.5,1],resolucao_baixa=False,revisao='',geracao_complementar=True))
# One generated rainy cloud supplies two perfectly aligned states, preserving generated alpha.
cloud=Image.open(cloud_path).convert('RGBA');dry=cloud.copy();ar=np.array(dry);ar[710:,:,3]=0;dry=Image.fromarray(ar,'RGBA')
cloud=trim_alpha(cloud)
# Shared scale and shared original frame: same cloud remains at exactly the same pixel position.
orig=Image.open(cloud_path).convert('RGBA');arr=np.array(orig);lab,n=ndi.label(arr[:,:,3]>16);sizes=np.bincount(lab.ravel());keep=sizes>100;keep[0]=False
support=ndi.binary_dilation(keep[lab],iterations=2);arr[~support,3]=0
box=Image.fromarray(arr).getbbox();wet=Image.fromarray(arr).crop(box);dry_arr=arr.copy();dry_arr[710:,:,3]=0;dry=Image.fromarray(dry_arr).crop(box)
size=(384,round(wet.height*384/wet.width))
for name,img in [('nuvem_chovendo',wet),('nuvem_parada',dry)]:
 img=img.resize(size,Image.Resampling.LANCZOS);can=Image.new('RGBA',(size[0]+16,size[1]+16));can.paste(img,(8,8))
 r=next(r for r in records if r['cenario']=='08_plantacao' and r['nome']==name);can.save(OUT/r['arquivo']);r.update(largura=can.width,altura=can.height,origem=cloud_path.name,recorte_origem=None,resolucao_baixa=False,revisao='',geracao_complementar=True,grupo_estados='nuvem_chovendo/nuvem_parada',pivo=[.5,1])
# Machine-readable metadata and visual reviews, all relative paths portable.
(OUT/'manifesto.json').write_text(json.dumps(dict(versao=1,total=len(records),itens_catalogo=380,extras=1,assets=records),ensure_ascii=False,indent=2))
with (OUT/'inventario.csv').open('w') as f:
 keys=['id','cenario','nome','tipo','arquivo','largura','altura','resolucao_baixa','revisao'];writer=csv.DictWriter(f,keys,extrasaction='ignore');writer.writeheader();writer.writerows(records)
for sc,*_ in CONFIG:
 items=[r for r in records if r['cenario']==sc];thumb=Image.new('RGB',(1000,((len(items)+3)//4)*220),'#243446');draw=ImageDraw.Draw(thumb)
 for j,r in enumerate(items):
  img=Image.open(OUT/r['arquivo']);img.thumbnail((230,177));x=(j%4)*250+(250-img.width)//2;y=(j//4)*220+5
  thumb.paste(img,(x,y),img);draw.text(((j%4)*250+7,(j//4)*220+188),r['nome'],fill='white')
 thumb.save(OUT/sc/'CONTATO.jpg',quality=90)
htmlrows=[]
for r in records:
 htmlrows.append('<article data-sc="'+r['cenario']+'"><img loading="lazy" src="'+r['arquivo']+'"><b>'+r['nome']+'</b><small>'+r['cenario']+' · '+str(r['largura'])+' × '+str(r['altura'])+' px</small><small>'+html.escape(r['revisao'])+'</small></article>')
(OUT/'catalogo.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Fazenda Capricho — PNGs individuais</title><style>body{font:16px system-ui;margin:24px;background:#faf6f0;color:#443044}header{position:sticky;top:0;background:#faf6f0;padding:12px;z-index:1}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}article{border-radius:14px;background:white;padding:12px;display:flex;flex-direction:column;gap:8px;border:1px solid #dfd4dc}img{height:190px;object-fit:contain;background-color:#263746;background-image:linear-gradient(45deg,#344758 25%,transparent 25%),linear-gradient(-45deg,#344758 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#344758 75%),linear-gradient(-45deg,transparent 75%,#344758 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}small{font-size:12px}select,input{padding:8px}</style><header><h1>Fazenda Capricho · 380 itens + 1 extra</h1><p>Recortes RGBA das pranchas 3D existentes. Resolução nativa; prévias separadas. Estados visuais ainda exigem validação.</p><input id="q" placeholder="Buscar peça"><select id="sc"><option value="">Todos os cenários</option>'''+''.join('<option>'+c[0]+'</option>' for c in CONFIG)+'''</select></header><main>'''+''.join(htmlrows)+'''</main><script>function filter(){document.querySelectorAll('article').forEach(e=>e.hidden=!(e.textContent.toLowerCase().includes(q.value.toLowerCase())&&(!sc.value||e.dataset.sc===sc.value)))}q.oninput=sc.onchange=filter;</script></html>''')
assert len(records)==381,len(records)
print('TOTAL',len(records))
