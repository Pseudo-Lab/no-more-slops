"""Finite notation-policy tests with simulated answers, not model accuracy."""
from types import SimpleNamespace

import numpy as np
import cv2
import pytest

from cad_api import connection_graph as graph
from cad_api import connection_semantics as semantics


def distribution(options, chosen, probability=.92):
    return {key: probability if key == chosen else (1-probability)/(len(options)-1) for key in options}


def test_category_requires_same_unique_meaning_in_both_orders():
    yes=distribution(semantics.LINE_OPTIONS, 'continuation')
    assert semantics.paired_category([yes,yes], semantics.LINE_OPTIONS)[0]=='continuation'
    assert semantics.paired_category([yes,distribution(semantics.LINE_OPTIONS,'junction')],semantics.LINE_OPTIONS)[0] is None
    assert semantics.paired_category([yes,None],semantics.LINE_OPTIONS)[0] is None
    assert semantics.paired_category([{'continuation':1},yes],semantics.LINE_OPTIONS)[0] is None


def test_underpass_never_accepts_a_turn_or_a_join():
    hypothesis={'kind':'crossing_underpass_no_join','axis':'horizontal','center':[50,50]}
    analysis={'hypotheses':[hypothesis]}
    positive=distribution(semantics.LINE_OPTIONS,'crossing_no_join')
    straight={'state':'review_needed','path':[[20,50],[80,50]],'reasons':[],'evidence':[]}
    semantics.apply_line_answer(straight,analysis,[positive,positive],['A','B'])
    assert straight['state']=='confirmed'
    turn={'state':'review_needed','path':[[20,50],[50,50],[50,80]],'reasons':[],'evidence':[]}
    semantics.apply_line_answer(turn,analysis,[positive,positive],['A','B'])
    assert turn['state']=='review_needed'
    joining=distribution(semantics.LINE_OPTIONS,'junction')
    semantics.apply_line_answer(turn,analysis,[joining,joining],['A','B'])
    assert turn['state']=='review_needed'


def test_dash_semantics_keeps_old_binary_rejection_visible():
    old={'p_yes':[.04,.08]}
    entity={'state':'rejected','path':[[10,50],[90,50]],'reasons':['strong_paired_rejection'],'evidence':[old]}
    analysis={'hypotheses':[{'kind':'dashed_continuation','axis':'horizontal'}]}
    answer=distribution(semantics.LINE_OPTIONS,'continuation')
    semantics.apply_line_answer(entity,analysis,[answer,answer],['A','B'])
    assert entity['state']=='confirmed' and entity['pre_semantic_state']=='rejected'
    assert entity['evidence']==[old] and entity['semantic_interpretation']['raw_distributions']==[answer,answer]


def test_unobserved_body_contact_cannot_be_confirmed_by_category():
    entity={'state':'review_needed','detail':{'contact_geometry_status':'unobserved'},'reasons':[]}
    answer=distribution(semantics.PORT_OPTIONS,'attached')
    semantics.apply_port_answer(entity,[answer,answer],['A','B'])
    assert entity['state']=='review_needed'


def test_composite_port_view_preserves_faint_original_ink_in_both_panels():
    page=np.full((150,170),255,np.uint8)
    page[30:80,40]=0
    page[79,40:70]=0
    page[80:85,55]=165
    page[88:95,55]=165
    crops=[]
    class View:
        def __init__(self,page,rect,scale):
            self.rect,self.s=rect,1
            self.img=np.zeros((rect[3]-rect[1],rect[2]-rect[0],3),np.uint8)
            crops.append((rect,self.img.shape))
        def p(self,x,y): return round(x-self.rect[0]),round(y-self.rect[1])
        def finish(self): return self.img
    extractor=SimpleNamespace(ScaledView=View,fit_scale=lambda *a,**kw:1,
        V=SimpleNamespace(crop=lambda p,x0,y0,x1,y1:p[y0:y1,x0:x1]))
    detail={'object':'s1','bbox':[40,30,70,79],'point':[55,79],
            'body_contact':[55,79],'line_anchor':[55,83],'outside_marker':[55,83],
            'path':[[55,79],[55,83]]}
    original=page.copy()
    image=semantics.semantic_port_view(extractor,page,detail,(230,0,0))
    offset=0
    for rect,shape in crops:
        raw=page[rect[1]:rect[3],rect[0]:rect[2]]
        panel=image[32:32+shape[0],offset:offset+shape[1]]
        assert np.array_equal(panel[raw<255],cv2.cvtColor(raw,cv2.COLOR_GRAY2BGR)[raw<255])
        offset+=shape[1]+12
    assert len(crops)==2 and np.array_equal(page,original)


def test_large_composite_fits_backend_image_dimensions_without_repainting(monkeypatch):
    panel=np.full((300,850,3),165,np.uint8)
    monkeypatch.setattr(graph,'raw_local_view',lambda *args:panel.copy())
    page=np.full((30,30),255,np.uint8)
    image=semantics.semantic_port_view(None,page,{'line_anchor':[10,10]},(230,0,0))
    assert max(image.shape[:2])<=1536
    assert (image==165).all(axis=2).sum()>100000 and (page==255).all()


class Judge:
    def __init__(self,line='continuation',port='attached',omit=False,route='line_only'):
        self.line,self.port,self.omit=line,port,omit
        self.calls=[]
        self.route=route
    async def ask_chunked(self,stage,state,questions,metadata):
        self.calls.append((stage,questions,metadata))
        options=(semantics.LINE_OPTIONS if stage=='K9_drawing_notation' else
                 semantics.ROUTE_OPTIONS if stage=='K11_semantic_route_context' else semantics.PORT_OPTIONS)
        chosen=(self.line if stage=='K9_drawing_notation' else
                self.route if stage=='K11_semantic_route_context' else self.port)
        return {name:distribution(options,chosen) for name in questions if not self.omit or not name.endswith('_B')}


@pytest.fixture
def example(monkeypatch):
    page=np.full((150,170),255,np.uint8);page[50,39:122]=90
    objects=[{'id':'s1','bbox':[20,40,39,60]},{'id':'s2','bbox':[121,40,140,60]}]
    line={'id':'line','kind':'segment','state':'review_needed','confidence':None,'reasons':[],
          'path':[[40,50],[120,50]],'geometry':{'path':[[40,50],[120,50]]},'detail':{},'candidate_indices':[0]}
    pa={'id':'pa','kind':'attachment','state':'review_needed','confidence':None,'reasons':[],
        'path':[[39,50],[40,50]],'geometry':{'object':0,'point':[39,50],'line_anchor':[40,50],'side':'right'},
        'detail':{'bbox':objects[0]['bbox'],'point':[39,50],'outside_marker':[40,50],'line_anchor':[40,50],
                  'object':0,'contact_geometry_status':'observed'},'candidate_indices':[0]}
    pb={'id':'pb','kind':'attachment','state':'confirmed','confidence':.9,'reasons':[],
        'path':[[121,50],[120,50]],'geometry':{'object':1,'point':[121,50],'line_anchor':[120,50],'side':'left'},
        'detail':{'contact_geometry_status':'observed'},'candidate_indices':[0]}
    record={'index':0,'parent_index':0,'entity_ids':['line','pa','pb'],'attachment_ids':['pa','pb'],
            'state':'review_needed','reasons':[],'path':line['path'],'baseline_accepted':False,'accepted':False}
    ctx=SimpleNamespace(kind='pid',page=page,text_h=9,tables=[],jev=Judge(),
        connection_graph={'entities':[line,pa,pb],'candidate_routes':[record],'alternative_routes':[],
                          'policy':{},'summary':{}})
    rel={'a':0,'b':1,'a_side':'right','b_side':'left','path':line['path'],'net':1,
         'accepted':False,'decision':'global_pair_local_uncertain','k3':[.8,.85]}
    extractor=SimpleNamespace(V=SimpleNamespace(RED=(0,0,230)),BLUE=(230,0,0),CG=None,
        choice=lambda state,criteria:{'state':state,'criteria':criteria},Img=lambda image:image)
    monkeypatch.setattr(graph,'raw_local_view',lambda *args:np.zeros((2,2,3),np.uint8))
    monkeypatch.setattr(semantics,'analyze_entity',lambda *args,**kwargs:{'eligible':True,
        'hypotheses':[{'kind':'dashed_continuation','axis':'horizontal'}]})
    return extractor,ctx,objects,rel,line,pa


@pytest.mark.asyncio
async def test_ports_are_reviewed_even_when_upstream_notation_is_uncertain(example):
    extractor,ctx,objects,rel,line,port=example
    ctx.jev=Judge(line='uncertain')
    result=await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert [call[0] for call in ctx.jev.calls]==['K9_drawing_notation','K10_semantic_actual_port']
    assert port['state']=='confirmed' and line['state']=='review_needed' and not rel['accepted']
    assert result['summary']['semantic_port_reviews']==1


@pytest.mark.asyncio
async def test_semantic_path_and_actual_ports_must_both_confirm(example):
    extractor,ctx,objects,rel,line,port=example
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert rel['accepted'] and rel['decision']=='semantic_drawing_route_with_actual_ports'
    assert rel['path']==[[40,50],[120,50]] and rel['net']==1
    assert rel['semantic_entity_ids']==['line','pa']
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert len(ctx.jev.calls)>=3


@pytest.mark.asyncio
@pytest.mark.parametrize('meaning,state',[('intervening_symbol','rejected'),
    ('uncertain','review_needed')])
async def test_full_route_veto_is_kept_when_local_elements_and_ports_confirm(example,meaning,state):
    extractor,ctx,objects,rel,line,port=example
    ctx.jev=Judge(route=meaning)
    result=await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert line['state']==port['state']=='confirmed' and not rel['accepted']
    assert result['candidate_routes'][0]['state']==state
    assert all(w['meaning']==meaning for w in rel['semantic_route_context']['windows'])
    assert rel['semantic_route_context']['meaning']==('intervening_symbol' if meaning=='intervening_symbol' else None)
    assert rel['path']==[[40,50],[120,50]]


@pytest.mark.asyncio
async def test_full_route_budget_cannot_accept_an_unasked_connection(example):
    extractor,ctx,objects,rel,line,port=example
    ctx.connection_semantic_route_context_budget=0
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert line['state']==port['state']=='confirmed' and not rel['accepted']
    assert rel['semantic_route_context']['state']=='review_needed'
    assert len(ctx.jev.calls)==2


@pytest.mark.asyncio
async def test_missing_order_and_independent_port_budget_do_not_create_a_link(example):
    extractor,ctx,objects,rel,line,port=example
    ctx.connection_semantic_line_budget=0
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert not rel['accepted'] and port['state']=='confirmed' and len(ctx.jev.calls)==1


@pytest.mark.asyncio
async def test_previous_accepted_pair_has_no_new_queries(example):
    extractor,ctx,objects,rel,line,port=example
    rel['accepted']=True
    ctx.jev=Judge(line='disconnected',port='passes_beside')
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert rel['accepted'] and not ctx.jev.calls


@pytest.mark.asyncio
async def test_selected_semantic_alternative_updates_parent_geometry_and_entity_references(example):
    extractor,ctx,objects,rel,line,port=example
    ctx.page[60,39:122]=90
    rel['route_alternatives']=[{'a':0,'b':1,'a_side':'right','b_side':'left',
        'a_point':[40,60],'b_point':[120,60],'path':[[40,60],[120,60]],'net':2}]
    alternative_line={**line,'id':'altline','path':[[40,60],[120,60]],
                      'geometry':{'path':[[40,60],[120,60]]},'candidate_indices':[1]}
    alternative_port={**port,'id':'altport','candidate_indices':[1],
                      'geometry':{'object':0,'point':[39,60],'line_anchor':[40,60],'side':'right'}}
    other_port={**ctx.connection_graph['entities'][2],'id':'altother','candidate_indices':[1]}
    ctx.connection_graph['entities'] += [alternative_line,alternative_port,other_port]
    ctx.connection_graph['alternative_routes']=[{'index':1,'parent_index':0,'alternative_index':0,
        'entity_ids':['altline','altport','altother'],'attachment_ids':['altport','altother'],
        'state':'review_needed','reasons':[],'path':[[40,60],[120,60]],'net':2,
        'baseline_accepted':False,'accepted':False}]
    class AlternativeJudge(Judge):
        async def ask_chunked(self,stage,state,questions,metadata):
            result=await super().ask_chunked(stage,state,questions,metadata)
            for name in questions:
                if name.startswith('smline_'):
                    result[name]=distribution(semantics.LINE_OPTIONS,'disconnected')
            return result
    ctx.jev=AlternativeJudge()
    result=await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert rel['accepted'] and rel['path']==[[40,60],[120,60]] and rel['net']==2
    assert rel['selected_semantic_alternative_index']==0
    assert rel['shared_graph_entity_ids']==['altline','altport','altother']
    assert rel['pre_semantic_route']['path']==[[40,50],[120,50]]
    parent=result['candidate_routes'][0]
    assert parent['path']==rel['path'] and parent['entity_ids']==rel['shared_graph_entity_ids']
    assert parent['pre_semantic_graph_path']==[[40,50],[120,50]]


@pytest.mark.asyncio
async def test_window_budget_does_not_clear_an_unreviewed_tail(example):
    extractor,ctx,objects,rel,line,port=example
    ctx.connection_semantic_window_budget=0
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    guard=rel['semantic_route_context']
    assert not rel['accepted'] and not guard['coverage_complete']
    assert guard['required_windows']>0 and not guard['windows']
    assert 'semantic_window_budget_exhausted' in guard['reasons']
    assert len(ctx.jev.calls)==2


@pytest.mark.asyncio
async def test_one_unresolved_overlapping_window_blocks_whole_route(example):
    extractor,ctx,objects,rel,line,port=example
    ctx.page=np.full((150,300),255,np.uint8)
    line['path']=rel['path']=[[40,50],[240,50]]
    ctx.connection_graph['candidate_routes'][0]['path']=line['path']
    class Partial(Judge):
        async def ask_chunked(self,stage,state,questions,metadata):
            result=await super().ask_chunked(stage,state,questions,metadata)
            if stage=='K11_semantic_route_context':
                for name in result:
                    if '_w1_' in name:
                        result[name]=distribution(semantics.ROUTE_OPTIONS,'uncertain')
            return result
    ctx.jev=Partial()
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    guard=rel['semantic_route_context']
    assert not rel['accepted'] and guard['coverage_complete']
    assert len(guard['windows'])==3
    assert [w['meaning'] for w in guard['windows']]==['line_only','uncertain','line_only']
    assert guard['state']=='review_needed'


@pytest.mark.asyncio
async def test_original_closed_endpoint_outline_cannot_be_promoted_by_local_answers(example,monkeypatch):
    extractor,ctx,objects,rel,line,port=example
    observed={'kind':'endpoint_outline_extension_suspected','state':'review_needed',
              'reason':'endpoint_outline_extension_requires_review','original_path':rel['path']}
    monkeypatch.setattr(semantics,'endpoint_outline_extension_proposals',lambda *args:[observed])
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert line['state']==port['state']=='confirmed' and not rel['accepted']
    guard=rel['semantic_route_context']
    assert guard['state']=='review_needed' and guard['outline_extension_hypotheses']==[observed]
    assert guard['required_windows']>0 and not guard['coverage_complete']
    assert len(ctx.jev.calls)==2


@pytest.mark.asyncio
async def test_old_confirmed_local_entity_cannot_override_raw_unjoined_axis_change(example,monkeypatch):
    extractor,ctx,objects,rel,line,port=example
    line.update(state='confirmed',confidence=.95)
    crossing={'kind':'raw_crossing_turn_requires_review','state':'review_needed',
              'reason':'axis_change_at_raw_no_join_crossing'}
    monkeypatch.setattr(semantics,'raw_corner_transition_proposals',lambda *a,**kw:[crossing])
    await semantics.verify_drawing_semantics(extractor,ctx,objects,[rel])
    assert line['state']==port['state']=='confirmed' and not rel['accepted']
    guard=rel['semantic_route_context']
    assert guard['crossing_transition_hypotheses']==[crossing]
    assert guard['state']=='review_needed' and not guard['coverage_complete']
    assert [call[0] for call in ctx.jev.calls]==['K10_semantic_actual_port']
