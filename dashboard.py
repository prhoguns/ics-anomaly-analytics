from pathlib import Path
import duckdb
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Industrial control anomaly analytics', layout='wide')
st.title('Industrial control anomaly analytics')
st.caption('HAI 21.03 · one second sensor readings · test1 attack intervals')
db = ROOT/'data/analytics.duckdb'
if not db.exists():
    st.error('Run scripts/download.py and scripts/build_db.py first.')
    st.stop()
con = duckdb.connect(str(db),read_only=True)
overview = con.execute("SELECT COUNT(*),SUM(attack) FROM readings WHERE split='test'").fetchone()
episodes = con.execute((ROOT/'sql/02_attack_episodes.sql').read_text()).df()
a,b,c = st.columns(3)
a.metric('Test seconds',f'{overview[0]:,}')
b.metric('Labeled attack seconds',f'{overview[1]:,}')
c.metric('Attack episodes',len(episodes))
st.subheader('Process telemetry')
sensors = [r[0] for r in con.execute('SELECT sensor FROM baseline ORDER BY sensor').fetchall()]
sensor = st.sidebar.selectbox('Sensor',sensors,index=sensors.index('P1_FT01'))
hours = con.execute("SELECT MIN(time),MAX(time) FROM readings WHERE split='test'").fetchone()
first_hour = hours[0]
hour = st.sidebar.slider('Hours from start',0,11,4)
start = first_hour + __import__('datetime').timedelta(hours=hour)
end = start + __import__('datetime').timedelta(hours=1)
trace = con.execute('''SELECT time,reading,attack,z_score FROM scores
 WHERE split='test' AND sensor=? AND time BETWEEN ? AND ?
 AND EXTRACT(EPOCH FROM time)::BIGINT % 5=0 ORDER BY time''',[sensor,start,end]).df()
trace['period'] = trace['attack'].map({0:'Normal',1:'Attack'})
st.plotly_chart(px.scatter(trace,x='time',y='reading',color='period',
 color_discrete_map={'Normal':'#0f766e','Attack':'#dc2626'},
 title=f'{sensor} readings in selected hour (every 5 seconds)'),use_container_width=True)
left,right = st.columns(2)
tradeoff = con.execute((ROOT/'sql/09_threshold_tradeoff.sql').read_text()).df()
left.plotly_chart(px.line(tradeoff,x='threshold',y=['recall_pct','alert_precision_pct'],markers=True,
 title='Simple maximum-z threshold tradeoff'),use_container_width=True)
outside = con.execute('''SELECT sensor,attack,100.0*AVG(outside_training_98pct::INT) outside_pct
 FROM scores WHERE split='test' GROUP BY 1,2''').df()
outside['period'] = outside['attack'].map({0:'Normal',1:'Attack'})
right.plotly_chart(px.bar(outside,x='sensor',y='outside_pct',color='period',barmode='group',
 title='Outside training normal range'),use_container_width=True)
st.subheader('Labeled attack episodes')
st.dataframe(episodes,use_container_width=True,hide_index=True)
st.caption('A high sensor deviation is an investigation cue, not proof of an attack. Training and test are separate operating periods; the threshold chart is descriptive, not a production detector.')
con.close()
