# -*- coding: utf-8 -*-
"""招聘AI助手 · 前端（app.py）
精美单页前端：AI助理（对话式指挥）· 简历录入 · 候选人台账 · 数据统计。
所有 /api/* 接口代理转发到后端 127.0.0.1:8010。
启动：python app.py  （访问 http://127.0.0.1:7860）
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

BACKEND = "http://127.0.0.1:8010"
app = FastAPI(title="招聘AI助手")

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>招聘AI助手</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --brand:#2563EB;--brand-2:#3B82F6;--dark:#0F172A;--dark-2:#1E293B;
  --bg:#F1F5F9;--card:#fff;--text:#1E293B;--muted:#64748B;
  --border:#E2E8F0;--green:#10B981;--red:#EF4444;--amber:#F59E0B;
}
body{font-family:"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;flex-direction:column;overflow:hidden}
/* ---------- Header ---------- */
header{height:64px;background:linear-gradient(135deg,#1D4ED8,#3B82F6 60%,#60A5FA);color:#fff;display:flex;align-items:center;padding:0 24px;gap:14px;flex-shrink:0;box-shadow:0 2px 12px rgba(37,99,235,.25);z-index:5}
.logo{width:38px;height:38px;border-radius:10px;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;font-size:20px}
header h1{font-size:19px;font-weight:700;letter-spacing:.5px}
header .sub{font-size:12px;opacity:.85;margin-top:1px}
.spacer{flex:1}
.status{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.15);padding:7px 14px;border-radius:20px;font-size:12.5px}
.dot{width:9px;height:9px;border-radius:50%;background:var(--green);box-shadow:0 0 0 3px rgba(16,185,129,.3)}
.dot.off{background:var(--red);box-shadow:0 0 0 3px rgba(239,68,68,.3)}
.model-pick{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.16);padding:6px 12px;border-radius:20px;font-size:12.5px;color:#fff}
.model-pick .mp-label{opacity:.9}
.model-pick select{background:transparent;border:none;color:#fff;font-size:12.5px;outline:none;cursor:pointer;max-width:190px;font-family:inherit}
.model-pick select option{color:#1E293B}
.toast{position:fixed;top:78px;right:24px;background:#0F172A;color:#fff;padding:11px 18px;border-radius:12px;font-size:13px;box-shadow:0 6px 20px rgba(15,23,42,.25);opacity:0;transform:translateY(-6px);transition:.25s;z-index:99;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
.attach-btn{width:52px;height:52px;flex-shrink:0;border:1px solid var(--border);border-radius:13px;background:var(--card);font-size:20px;cursor:pointer;transition:.15s}
.attach-btn:hover{background:#EFF6FF;border-color:#BFDBFE}
.up-hint{font-size:12.5px;color:var(--muted)}
/* ---------- 登录页 ---------- */
#loginPage{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0F172A 0%,#1D4ED8 55%,#3B82F6 100%);overflow-y:auto;padding:20px}
.login-card{width:400px;max-width:94vw;background:rgba(255,255,255,.98);border-radius:22px;padding:34px 34px 28px;box-shadow:0 24px 60px rgba(15,23,42,.4);margin:auto}
.login-brand{text-align:center;margin-bottom:22px}
.login-logo{width:56px;height:56px;margin:0 auto 12px;border-radius:16px;background:linear-gradient(135deg,#2563EB,#60A5FA);display:flex;align-items:center;justify-content:center;font-size:28px;box-shadow:0 8px 20px rgba(37,99,235,.35)}
.login-title{font-size:21px;font-weight:800;color:var(--text)}
.login-sub{font-size:12px;color:var(--muted);margin-top:3px}
.login-tabs{display:flex;background:#F1F5F9;border-radius:12px;padding:4px;margin-bottom:20px}
.login-tab{flex:1;text-align:center;padding:9px 0;border-radius:9px;font-size:14px;font-weight:600;color:var(--muted);cursor:pointer;transition:.15s}
.login-tab.active{background:#fff;color:var(--brand);box-shadow:0 2px 8px rgba(15,23,42,.08)}
.login-form label{font-size:12.5px;color:#334155;font-weight:600;margin:12px 0 5px;display:block}
.login-form input{width:100%;border:1px solid var(--border);border-radius:11px;padding:12px 13px;font-size:14px;outline:none;transition:.15s;background:#fff;box-sizing:border-box}
.login-form input:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(37,99,235,.12)}
.login-err{color:var(--red);font-size:12.5px;min-height:18px;margin-top:8px}
.login-btn{width:100%;margin-top:6px;border:none;border-radius:12px;padding:13px 0;font-size:15px;font-weight:700;color:#fff;background:linear-gradient(135deg,#2563EB,#3B82F6);cursor:pointer;transition:.15s;box-shadow:0 6px 16px rgba(37,99,235,.3)}
.login-btn:hover{transform:translateY(-1px)}
.login-btn:disabled{opacity:.6;cursor:not-allowed}
.login-hint{text-align:center;font-size:12px;color:var(--muted);margin-top:14px}
/* ---------- Header 用户区 ---------- */
.user-box{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.15);padding:5px 12px 5px 8px;border-radius:20px;font-size:13px;color:#fff}
.u-avatar{width:26px;height:26px;border-radius:50%;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:14px}
.u-logout{border:none;background:rgba(255,255,255,.18);color:#fff;border-radius:14px;padding:5px 12px;font-size:12px;cursor:pointer;transition:.15s}
.u-logout:hover{background:rgba(255,255,255,.32)}
/* ---------- Layout ---------- */
.wrap{flex:1;display:flex;overflow:hidden}
nav{width:216px;background:var(--card);border-right:1px solid var(--border);padding:16px 12px;display:flex;flex-direction:column;gap:6px;flex-shrink:0}
.nav-group{font-size:11px;color:var(--muted);padding:8px 12px 4px;letter-spacing:1px}
.nav-item{display:flex;align-items:center;gap:11px;padding:11px 13px;border-radius:11px;cursor:pointer;font-size:14px;color:#334155;transition:.15s;user-select:none}
.nav-item .ic{font-size:17px;width:22px;text-align:center}
.nav-item:hover{background:#EFF6FF}
.nav-item.active{background:linear-gradient(135deg,#2563EB,#3B82F6);color:#fff;box-shadow:0 4px 12px rgba(37,99,235,.3)}
main{flex:1;overflow-y:auto;padding:22px;min-width:0}
.page{display:none;max-width:1060px;margin:0 auto}
.page.active{display:block}
.page-title{font-size:18px;font-weight:700;margin-bottom:4px}
.page-desc{font-size:13px;color:var(--muted);margin-bottom:18px}
/* ---------- Chat ---------- */
.chat-shell{display:flex;flex-direction:column;height:calc(100vh - 64px - 44px);min-height:480px}
.chat-box{flex:1;background:var(--card);border:1px solid var(--border);border-radius:16px;overflow-y:auto;padding:22px;display:flex;flex-direction:column;gap:16px}
.msg{display:flex;gap:10px;max-width:86%}
.msg.user{align-self:flex-end;flex-direction:row-reverse}
.avatar{width:32px;height:32px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:15px;color:#fff}
.msg.user .avatar{background:linear-gradient(135deg,#2563EB,#60A5FA)}
.msg.ai .avatar{background:linear-gradient(135deg,#0F172A,#334155)}
.bubble{padding:11px 15px;border-radius:16px;font-size:14px;line-height:1.65;white-space:pre-wrap;word-break:break-word}
.msg.user .bubble{background:linear-gradient(135deg,#2563EB,#3B82F6);color:#fff;border-bottom-right-radius:4px}
.msg.ai .bubble{background:#F8FAFC;border:1px solid var(--border);color:var(--text);border-bottom-left-radius:4px}
.msg.ai .bubble b{color:var(--brand)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:2px}
.chip{background:#EFF6FF;border:1px solid #BFDBFE;color:#1D4ED8;border-radius:20px;padding:7px 13px;font-size:12.5px;cursor:pointer;transition:.15s}
.chip:hover{background:#DBEAFE}
.input-row{display:flex;gap:10px;margin-top:12px;align-items:flex-end}
#chatInput{flex:1;resize:none;border:1px solid var(--border);border-radius:13px;padding:13px 16px;font-size:14px;font-family:inherit;outline:none;transition:.15s;min-height:52px;max-height:140px;background:var(--card)}
#chatInput:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(37,99,235,.12)}
#sendBtn{height:52px;padding:0 24px;border:none;border-radius:13px;background:linear-gradient(135deg,#2563EB,#3B82F6);color:#fff;font-size:14.5px;font-weight:600;cursor:pointer;transition:.15s;box-shadow:0 4px 12px rgba(37,99,235,.3);flex-shrink:0}
#sendBtn:hover{transform:translateY(-1px)}
#sendBtn:disabled{opacity:.55;cursor:not-allowed;transform:none}
.typing{display:flex;align-items:center;gap:5px;padding:4px 2px}
.typing span{width:7px;height:7px;border-radius:50%;background:#94A3B8;animation:blink 1.2s infinite}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,80%,100%{opacity:.25}40%{opacity:1}}
/* ---------- Cards / forms / table ---------- */
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px;box-shadow:0 1px 3px rgba(15,23,42,.05)}
label{display:block;font-size:13px;color:#334155;font-weight:600;margin:14px 0 6px}
label:first-child{margin-top:0}
input[type=text],select,textarea{width:100%;border:1px solid var(--border);border-radius:11px;padding:11px 13px;font-size:14px;font-family:inherit;outline:none;background:#fff;transition:.15s}
input[type=text]:focus,select:focus,textarea:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(37,99,235,.12)}
.btn{border:none;border-radius:11px;padding:11px 22px;font-size:14px;font-weight:600;cursor:pointer;transition:.15s}
.btn.primary{background:linear-gradient(135deg,#2563EB,#3B82F6);color:#fff;box-shadow:0 4px 12px rgba(37,99,235,.25)}
.btn.primary:hover{transform:translateY(-1px)}
.btn.ghost{background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE}
.btn.ghost:hover{background:#DBEAFE}
.stat-grid{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:18px}
.stat-card{flex:1 1 200px;min-width:180px;background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px;box-shadow:0 1px 3px rgba(15,23,42,.05)}
.stat-card .num{font-size:32px;font-weight:800;margin-top:6px}
.stat-card .lbl{font-size:13px;color:var(--muted)}
.bar-row{display:flex;align-items:center;gap:10px;margin:9px 0;font-size:13px}
.bar-row .k{width:110px;color:#334155;flex-shrink:0}
.bar-track{flex:1;height:10px;background:#F1F5F9;border-radius:6px;overflow:hidden}
.bar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,#3B82F6,#60A5FA)}
.bar-row .v{width:60px;text-align:right;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:#F8FAFC;color:#475569;text-align:left;padding:11px 12px;font-weight:600;border-bottom:1px solid var(--border);white-space:nowrap;position:sticky;top:0}
td{padding:10px 12px;border-bottom:1px solid #F1F5F9;vertical-align:middle}
tr:hover td{background:#F8FAFC}
.tag{display:inline-block;padding:3px 10px;border-radius:14px;font-size:12px;font-weight:600}
.tag.blue{background:#DBEAFE;color:#1D4ED8}
.tag.green{background:#D1FAE5;color:#047857}
.tag.amber{background:#FEF3C7;color:#B45309}
.tag.gray{background:#F1F5F9;color:#64748B}
.tag.red{background:#FEE2E2;color:#B91C1C}
.empty{text-align:center;color:var(--muted);padding:50px 0;font-size:14px}
.toolbar{display:flex;gap:10px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
.toolbar input{width:260px}
.table-wrap{overflow:auto;max-height:calc(100vh - 230px);border-radius:16px}
.result-box{margin-top:14px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:11px;padding:12px 15px;font-size:13.5px;color:#166534;white-space:pre-wrap;line-height:1.6}
.result-box.err{background:#FEF2F2;border-color:#FECACA;color:#991B1B}
.suggest-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin-top:14px}
.suggest-grid .sg{background:#F8FAFC;border:1px solid var(--border);border-radius:11px;padding:12px 14px;font-size:13px;cursor:pointer;color:#334155;transition:.15s}
.suggest-grid .sg:hover{border-color:var(--brand);background:#EFF6FF}
@media(max-width:760px){nav{display:none}.wrap{flex-direction:column}.chat-shell{height:calc(100vh - 64px - 40px)}}
</style>
</head>
<body>
<!-- 登录 / 注册页 -->
<div id="loginPage">
  <div class="login-card">
    <div class="login-brand">
      <div class="login-logo">🤖</div>
      <div class="login-title">招聘AI助手</div>
      <div class="login-sub">Recruit Assistant · 每位用户独立数据</div>
    </div>
    <div class="login-tabs">
      <div class="login-tab active" data-tab="login">登录</div>
      <div class="login-tab" data-tab="reg">注册</div>
    </div>
    <div class="login-form" id="formLogin">
      <label>用户名</label>
      <input type="text" id="lgUser" placeholder="输入用户名" autocomplete="username">
      <label>密码</label>
      <input type="password" id="lgPass" placeholder="输入密码" autocomplete="current-password">
      <div class="login-err" id="lgErr"></div>
      <button class="login-btn" id="lgBtn">登 录</button>
      <div class="login-hint">演示账号：admin / 123456</div>
    </div>
    <div class="login-form" id="formReg" style="display:none">
      <label>用户名</label>
      <input type="text" id="rgUser" placeholder="2-20 个字符" autocomplete="username">
      <label>密码</label>
      <input type="password" id="rgPass" placeholder="至少 6 位" autocomplete="new-password">
      <label>确认密码</label>
      <input type="password" id="rgPass2" placeholder="再次输入密码">
      <div class="login-err" id="rgErr"></div>
      <button class="login-btn" id="rgBtn">注 册</button>
    </div>
  </div>
</div>
<header>
  <div class="logo">🤖</div>
  <div>
    <h1>招聘AI助手</h1>
    <div class="sub">Recruit Assistant · 对话式指挥</div>
  </div>
  <div class="spacer"></div>
  <div class="model-pick"><span class="mp-label">模型</span><select id="modelSelect"><option>加载中…</option></select></div>
  <div class="status"><span class="dot" id="dot"></span><span id="statusTxt">连接后端…</span></div>
  <div class="user-box"><span class="u-avatar" id="uAvatar">👤</span><span id="userName">—</span><button class="u-logout" id="logoutBtn">退出</button></div>
</header>

<div class="wrap">
  <nav>
    <div class="nav-group">工作台</div>
    <div class="nav-item active" data-page="chat"><span class="ic">💬</span>AI 助理</div>
    <div class="nav-item" data-page="resume"><span class="ic">📥</span>简历录入</div>
    <div class="nav-item" data-page="records"><span class="ic">📋</span>候选人台账</div>
    <div class="nav-item" data-page="stats"><span class="ic">📊</span>数据统计</div>
  </nav>

  <main>
    <!-- 聊天页 -->
    <div class="page active" id="page-chat">
      <div class="chat-shell">
        <div class="chat-box" id="chatBox"></div>
        <div class="chips" id="chips"></div>
        <div class="input-row">
          <button class="attach-btn" id="sendFileBtn" title="发送简历文件（PDF/Word/TXT）">📎</button>
          <textarea id="chatInput" rows="1" placeholder="输入指令，例如：给算法工程师岗位生成一条打招呼话术…"></textarea>
          <button id="sendBtn">发送</button>
        </div>
        <input type="file" id="fileSend" accept=".pdf,.docx,.doc,.txt" style="display:none">
      </div>
    </div>

    <!-- 简历录入页 -->
    <div class="page" id="page-resume">
      <div class="page-title">📥 简历解析录入</div>
      <div class="page-desc">粘贴简历文本，系统自动抽取姓名/手机号/期望薪资/到岗时间，自动查重后写入台账。</div>
      <div class="card">
        <div style="display:flex;gap:16px;flex-wrap:wrap">
          <div style="flex:1 1 200px"><label>岗位名称</label><input type="text" id="r_post" placeholder="如：算法工程师"></div>
          <div style="flex:1 1 200px"><label>简历来源</label>
            <select id="r_channel">
              <option>BOSS直聘</option><option>前程无忧</option><option>智联招聘</option><option>猎聘</option>
              <option>拉勾</option><option>脉脉</option><option>牛客</option><option>实习僧</option>
              <option>大街网</option><option>58同城</option><option>领英LinkedIn</option><option>邮箱投递</option>
              <option>官网投递</option><option>内推</option><option>猎头推荐</option><option>现场招聘会</option><option>其他</option>
            </select>
          </div>
        </div>
        <label>简历文本（可粘贴，也可上传文档自动读取）</label>
        <textarea id="r_text" rows="10" placeholder="在此粘贴候选人简历文本，或点击下方「上传简历文档」读取 PDF/Word…"></textarea>
        <div style="display:flex;gap:10px;align-items:center;margin-top:16px;flex-wrap:wrap">
          <button class="btn ghost" id="r_upBtn">📄 上传简历文档</button>
          <button class="btn primary" id="r_btn">解析并存入台账</button>
          <span class="up-hint" id="r_upHint"></span>
        </div>
        <input type="file" id="r_file" accept=".pdf,.docx,.doc,.txt" style="display:none">
        <div class="result-box" id="r_result" style="display:none"></div>
      </div>
      <div class="suggest-grid">
        <div class="sg" data-fill="这份简历录入到算法工程师岗位，来源BOSS直聘：

【个人简介】张三，5年算法经验，期望薪资25k，一周内到岗，电话13800138000。">💡 快捷示例：一句话完成录入</div>
        <div class="sg" data-page-jump="chat">💬 也可以直接去 AI 助理对话录入</div>
      </div>
    </div>

    <!-- 台账页 -->
    <div class="page" id="page-records">
      <div class="page-title">📋 候选人台账</div>
      <div class="page-desc">所有已录入候选人明细，可搜索筛选。</div>
      <div class="toolbar">
        <input type="text" id="recSearch" placeholder="🔍 搜索姓名 / 手机号 / 岗位 / 渠道…">
        <button class="btn ghost" id="recRefresh">刷新</button>
      </div>
      <div class="table-wrap card"><table id="recTable"><tbody><tr><td class="empty">加载中…</td></tr></tbody></table></div>
    </div>

    <!-- 统计页 -->
    <div class="page" id="page-stats">
      <div class="page-title">📊 数据统计</div>
      <div class="page-desc">候选人数量与状态分布。</div>
      <div class="stat-grid" id="statGrid"></div>
      <div class="card" id="statDetail"></div>
    </div>
  </main>
</div>

<script>
const $=s=>document.querySelector(s);
const BACKEND_OK={ok:false};

/* ---------- 登录 / 鉴权 ---------- */
let TOKEN=localStorage.getItem('ra_token')||'';
let USERNAME=localStorage.getItem('ra_user')||'';
async function api(path,opts={}){
  const headers=Object.assign({'Content-Type':'application/json'},opts.headers||{});
  if(TOKEN)headers['Authorization']='Bearer '+TOKEN;
  const r=await fetch(path,Object.assign({},opts,{headers}));
  if(r.status===401){showLogin();throw new Error('未登录或登录已过期');}
  return r;
}
function showLogin(){$('#loginPage').style.display='flex';}
function hideLogin(){$('#loginPage').style.display='none';}
async function uploadFile(file){
  const fd=new FormData();fd.append('file',file);
  const r=await fetch('/api/upload_file',{method:'POST',headers:TOKEN?{'Authorization':'Bearer '+TOKEN}:{},body:fd});
  if(r.status===401){showLogin();throw new Error('未登录');}
  return r.json();
}
function refreshMain(){
  $('#userName').textContent=USERNAME;
  loadModels();checkBackend();
  document.querySelectorAll('.nav-item')[0]?.click();
}
async function doLogin(){
  const u=$('#lgUser').value.trim(),p=$('#lgPass').value;
  $('#lgErr').textContent='';$('#lgBtn').disabled=true;
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})});
    const d=await r.json();
    if(d.ok){TOKEN=d.token;USERNAME=d.username;localStorage.setItem('ra_token',TOKEN);localStorage.setItem('ra_user',USERNAME);hideLogin();refreshMain();}
    else{$('#lgErr').textContent=d.msg||'登录失败';}
  }catch(e){$('#lgErr').textContent='无法连接后端：'+e.message;}
  finally{$('#lgBtn').disabled=false;}
}
async function doRegister(){
  const u=$('#rgUser').value.trim(),p=$('#rgPass').value,p2=$('#rgPass2').value;
  $('#rgErr').textContent='';
  if(p!==p2){$('#rgErr').textContent='两次输入的密码不一致';return;}
  $('#rgBtn').disabled=true;
  try{
    const r=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})});
    const d=await r.json();
    if(d.ok){$('#rgErr').style.color='var(--green)';$('#rgErr').textContent=d.msg+'，请登录。';switchTab('login');}
    else{$('#rgErr').textContent=d.msg||'注册失败';}
  }catch(e){$('#rgErr').textContent='无法连接后端：'+e.message;}
  finally{$('#rgBtn').disabled=false;}
}
function switchTab(t){
  document.querySelectorAll('.login-tab').forEach(x=>x.classList.toggle('active',x.dataset.tab===t));
  $('#formLogin').style.display=t==='login'?'block':'none';
  $('#formReg').style.display=t==='reg'?'block':'none';
}
document.querySelectorAll('.login-tab').forEach(x=>x.onclick=()=>switchTab(x.dataset.tab));
$('#lgBtn').onclick=doLogin;
$('#rgBtn').onclick=doRegister;
$('#logoutBtn').onclick=async()=>{
  try{await fetch('/api/logout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:TOKEN})});}catch(e){}
  TOKEN='';USERNAME='';localStorage.removeItem('ra_token');localStorage.removeItem('ra_user');
  showLogin();
};
['lgUser','lgPass'].forEach(id=>document.getElementById(id).addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();}));
['rgUser','rgPass','rgPass2'].forEach(id=>document.getElementById(id).addEventListener('keydown',e=>{if(e.key==='Enter')doRegister();}));
/* 初始化：有 token 则自动登录，否则显示登录页 */
(async()=>{
  if(!TOKEN){showLogin();return;}
  try{
    const r=await fetch('/api/me',{headers:TOKEN?{'Authorization':'Bearer '+TOKEN}:{},signal:AbortSignal.timeout(6000)});
    if(r.status===200){const d=await r.json();USERNAME=d.username||USERNAME;localStorage.setItem('ra_user',USERNAME);hideLogin();refreshMain();}
    else{TOKEN='';localStorage.removeItem('ra_token');showLogin();}
  }catch(e){showLogin();}
})();

/* ---------- 页面切换 ---------- */
document.querySelectorAll('.nav-item').forEach(n=>n.onclick=()=>{
  document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
  n.classList.add('active');
  $('#page-'+n.dataset.page).classList.add('active');
  if(n.dataset.page==='records')loadRecords();
  if(n.dataset.page==='stats')loadStats();
});
document.querySelectorAll('.sg[data-page-jump]').forEach(s=>s.onclick=()=>{
  document.querySelectorAll('.nav-item').forEach(n=>n.dataset.page==='chat'&&n.click());
});

/* ---------- 模型切换 ---------- */
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(t._timer);t._timer=setTimeout(()=>t.classList.remove('show'),2200);}
async function loadModels(){
  try{
    const r=await api('/api/model',{signal:AbortSignal.timeout(8000)});
    const d=await r.json();
    const sel=$('#modelSelect');sel.innerHTML='';
    (d.models||[]).forEach(m=>{
      const o=document.createElement('option');o.value=m;o.textContent=m;
      if(m===d.current)o.selected=true;sel.appendChild(o);
    });
    sel.onchange=async()=>{
      const m=sel.value;
      try{
        const r=await api('/api/model',{method:'POST',body:JSON.stringify({model:m})});
        const d=await r.json();
        if(d.ok){toast('已切换模型：'+d.current);}
        else{toast('切换失败：'+(d.msg||'未知模型'));loadModels();}
      }catch(e){toast('切换失败：'+e.message);}
    };
  }catch(e){$('#modelSelect').innerHTML='<option>模型加载失败</option>';}
}

/* ---------- 后端健康检查 ---------- */
async function checkBackend(){
  try{const r=await fetch('/api/me',{headers:TOKEN?{'Authorization':'Bearer '+TOKEN}:{},signal:AbortSignal.timeout(5000)});
    if(r.status===200||r.status===401){$('#dot').classList.remove('off');$('#statusTxt').textContent='后端在线';BACKEND_OK.ok=true;}
    else{$('#dot').classList.add('off');$('#statusTxt').textContent='后端异常';}
  }catch(e){$('#dot').classList.add('off');$('#statusTxt').textContent='后端未连接';}
}
setInterval(checkBackend,15000);checkBackend();

/* ---------- 聊天 ---------- */
const chips=['今天新增了哪些候选人？','给算法工程师岗位生成一条初次打招呼的话术','统计一下各岗位的候选人数量','把王五的状态改为已邀约','台账里有哪些岗位在招？','帮我看看“未获取”姓名的候选人'];
let history=[];
$('#chips').innerHTML=chips.map(c=>'<div class="chip">'+c+'</div>').join('');
document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{$('#chatInput').value=c.textContent;sendMsg();});

function appendMsg(role,text){
  const box=$('#chatBox');
  const d=document.createElement('div');
  d.className='msg '+role;
  const av=role==='user'?'👤':'🤖';
  const esc=text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  d.innerHTML='<div class="avatar">'+av+'</div><div class="bubble"></div>';
  d.querySelector('.bubble').textContent=text;
  box.appendChild(d);box.scrollTop=box.scrollHeight;
  if(document.querySelector('.msg.typing'))document.querySelector('.msg.typing').remove();
}
function showTyping(){
  const box=$('#chatBox');const d=document.createElement('div');
  d.className='msg ai typing-msg';
  d.innerHTML='<div class="avatar">🤖</div><div class="bubble typing"><span></span><span></span><span></span></div>';
  box.appendChild(d);box.scrollTop=box.scrollHeight;
}
async function sendText(content, display){
  if(display)appendMsg('user',display);
  history.push({role:'user',content:content});
  $('#sendBtn').disabled=true;showTyping();
  try{
    const r=await api('/api/agent_chat',{method:'POST',body:JSON.stringify({messages:history})});
    const data=await r.json();
    const reply=data.reply||'（无回复）';
    document.querySelector('.typing-msg')?.remove();
    appendMsg('ai',reply);history.push({role:'assistant',content:reply});
  }catch(e){
    document.querySelector('.typing-msg')?.remove();
    appendMsg('ai','😵 调用失败：'+e.message);
  }finally{$('#sendBtn').disabled=false;}
}
function sendMsg(){
  const t=$('#chatInput').value.trim();if(!t)return;
  $('#chatInput').value='';sendText(t,t);
}
$('#sendBtn').onclick=sendMsg;
$('#chatInput').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}});
/* 发送文件给 AI 助理 */
$('#sendFileBtn').onclick=()=>$('#fileSend').click();
$('#fileSend').onchange=async()=>{
  const f=$('#fileSend').files[0];if(!f)return;
  $('#fileSend').value='';
  try{
    const d=await uploadFile(f);
    if(!d.text){toast('读取文件失败');return;}
    const text=(d.text||'').slice(0,15000);
    sendText('[附件：'+d.filename+']\n'+text, '[附件：'+d.filename+'（'+d.chars+'字）已发送，你可以继续指挥，例如"把这份简历录入到XX岗位"');
  }catch(e){toast('上传失败：'+e.message);}
};
appendMsg('ai','你好，我是招聘AI助手 🤖\n你可以直接用一句话指挥我：\n· 录入/更新简历\n· 查询候选人、台账、统计\n· 生成沟通话术\n· 更新状态、删除候选人\n在下方输入框输入，或点击快捷指令试试。');

/* ---------- 简历录入 ---------- */
document.querySelectorAll('.sg[data-fill]').forEach(s=>s.onclick=()=>{
  const lines=s.dataset.fill.split('\n');$('#r_post').value=lines[0].split('到')[0].replace('这份简历录入','').trim();
  const m=lines[0].match(/来源(\S+)/);if(m)$('#r_channel').value=m[1].replace(/[，,]/g,'');
  $('#r_text').value=lines.slice(1).join('\n');
});
/* 上传简历文档 → 提取文本填入简历文本框 */
$('#r_upBtn').onclick=()=>$('#r_file').click();
$('#r_file').onchange=async()=>{
  const f=$('#r_file').files[0];if(!f)return;
  const h=$('#r_upHint');h.textContent='正在读取 '+f.name+' …';
  try{
    const d=await uploadFile(f);
    if(!d.text){h.textContent='读取失败：该文件没有可解析的文字（可能是扫描版PDF）';}
    else{$('#r_text').value=d.text;h.textContent='已读取 '+d.filename+'（'+d.chars+'字），可编辑后点击「解析并存入台账」';}
  }catch(e){h.textContent='读取失败：'+e.message;}
  $('#r_file').value='';
};
$('#r_btn').onclick=async()=>{
  const post=$('#r_post').value.trim(),channel=$('#r_channel').value,text=$('#r_text').value.trim();
  const box=$('#r_result');
  if(!post||!text){box.className='result-box err';box.style.display='block';box.textContent='请填写岗位名称和简历文本。';return;}
  box.className='result-box';box.style.display='block';box.textContent='正在解析…';
  try{
    const r=await api('/api/resume_add',{method:'POST',
      body:JSON.stringify({post_name:post,channel:channel,resume_text:text,mode:'auto',target_key:null})});
    const d=await r.json();
    let msg='';
    if(d.duplicate){box.className='result-box err';msg='⚠️ 检测到该候选人已存在，未写入：\n'+(d.exists||[]).map(e=>e.name+'（'+e.phone+'）').join('、')+'\n可去 AI 助理对话中指定更新该候选人。';}
    else{msg=d.msg+'\n\n解析结果：'+JSON.stringify(d.parsed||{},null,2);}
    box.textContent=msg;
  }catch(e){box.className='result-box err';box.textContent='调用失败：'+e.message;}
};

/* ---------- 台账 ---------- */
let allRec=[];
async function loadRecords(){
  const tb=$('#recTable');tb.innerHTML='<tr><td class="empty">加载中…</td></tr>';
  try{
    const r=await api('/api/records');allRec=await r.json();
    renderRecords();
  }catch(e){tb.innerHTML='<tr><td class="empty">加载失败：'+e.message+'</td></tr>';}
}
function renderRecords(){
  const kw=($('#recSearch').value||'').trim();
  const list=allRec.filter(x=>!kw||JSON.stringify(x).toLowerCase().includes(kw.toLowerCase()));
  const heads=['岗位名称','候选人姓名','手机号','招聘渠道','期望薪资','到岗时间','沟通状态','面试时间','面试结果','备注'];
  const tb=$('#recTable');
  if(!list.length){tb.innerHTML='<tr><td class="empty">暂无数据</td></tr>';return;}
  let html='<tr>'+heads.map(h=>'<th>'+h+'</th>').join('')+'</tr>';
  const tagOf=(k,v)=>{
    if(k==='沟通状态')return v==='待沟通'?'<span class="tag gray">'+v+'</span>':v==='已邀约'?'<span class="tag blue">'+v+'</span>':'<span class="tag amber">'+v+'</span>';
    if(k==='面试结果')return v==='通过'?'<span class="tag green">'+v+'</span>':v==='不通过'?'<span class="tag red">'+v+'</span>':'<span class="tag gray">'+v+'</span>';
    return v;
  };
  list.forEach(x=>{
    html+='<tr>'+heads.map(h=>'<td>'+tagOf(h,x[h]||'')+'</td>').join('')+'</tr>';
  });
  tb.innerHTML=html;
}
$('#recSearch').addEventListener('input',renderRecords);
$('#recRefresh').onclick=loadRecords;

/* ---------- 统计 ---------- */
async function loadStats(){
  try{
    const r=await api('/api/stats');const d=await r.json();
    $('#statGrid').innerHTML=
      '<div class="stat-card"><div class="lbl">候选人总数</div><div class="num" style="color:var(--brand)">'+d.total+'</div></div>'+
      '<div class="stat-card"><div class="lbl">沟通状态分类</div><div class="num" style="color:var(--amber);font-size:20px">'+Object.keys(d.by_status||{}).length+' 类</div></div>'+
      '<div class="stat-card"><div class="lbl">面试结果分类</div><div class="num" style="color:var(--green);font-size:20px">'+Object.keys(d.by_result||{}).length+' 类</div></div>';
    let h='<div style="font-weight:700;font-size:15px;margin-bottom:10px">按沟通状态</div>';
    const maxS=Math.max(1,...Object.values(d.by_status||{}));
    Object.entries(d.by_status||{}).forEach(([k,v])=>h+='<div class="bar-row"><div class="k">'+k+'</div><div class="bar-track"><div class="bar-fill" style="width:'+(v/maxS*100)+'%"></div></div><div class="v">'+v+'人</div></div>');
    h+='<div style="font-weight:700;font-size:15px;margin:18px 0 10px">按面试结果</div>';
    const maxR=Math.max(1,...Object.values(d.by_result||{}));
    Object.entries(d.by_result||{}).forEach(([k,v])=>h+='<div class="bar-row"><div class="k">'+k+'</div><div class="bar-track"><div class="bar-fill" style="width:'+(v/maxR*100)+'%"></div></div><div class="v">'+v+'人</div></div>');
    $('#statDetail').innerHTML=h;
  }catch(e){$('#statGrid').innerHTML='<div class="empty">加载失败：'+e.message+'</div>';$('#statDetail').innerHTML='';}
}
</script>
<div class="toast" id="toast"></div>
</body>
</html>
"""


def _auth_headers(request):
    """从请求中提取 Authorization 头，用于代理转发。"""
    auth = request.headers.get("Authorization", "")
    return {"Authorization": auth} if auth else {}


def _proxy(url, method="GET", payload=None, timeout=180, headers=None):
    h = headers or {}
    if method == "POST":
        resp = requests.post(f"{BACKEND}{url}", json=payload, timeout=timeout, headers=h)
    else:
        resp = requests.get(f"{BACKEND}{url}", timeout=timeout, headers=h)
    if resp.status_code >= 400:
        # 透传后端错误状态（如 401 未登录），不转成 500
        try:
            content = resp.json()
        except Exception:
            content = {"detail": resp.text}
        return JSONResponse(status_code=resp.status_code, content=content)
    return resp.json()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    return HTML_PAGE


@app.post("/api/agent_chat")
async def api_agent_chat(request: Request):
    body = await request.json()
    return _proxy("/agent_chat", "POST", body, timeout=300, headers=_auth_headers(request))


@app.get("/api/records")
async def api_records(request: Request):
    return _proxy("/get_all_record", headers=_auth_headers(request))


@app.get("/api/stats")
async def api_stats(request: Request):
    return _proxy("/stat_count", headers=_auth_headers(request))


@app.post("/api/resume_add")
async def api_resume_add(request: Request):
    body = await request.json()
    return _proxy("/resume_parse_add", "POST", body, timeout=180, headers=_auth_headers(request))


@app.post("/api/update_status")
async def api_update_status(request: Request):
    body = await request.json()
    return _proxy("/update_status", "POST", body, headers=_auth_headers(request))


@app.post("/api/delete_candidate")
async def api_delete_candidate(request: Request):
    body = await request.json()
    return _proxy("/delete_candidate", "POST", body, headers=_auth_headers(request))


@app.get("/api/candidates")
async def api_candidates(request: Request):
    return _proxy("/get_candidate_names", headers=_auth_headers(request))


@app.get("/api/jobs")
async def api_jobs(request: Request):
    return _proxy("/get_job_list", headers=_auth_headers(request))


@app.get("/api/model")
async def api_model_get(request: Request):
    return _proxy("/model", headers=_auth_headers(request))


@app.post("/api/model")
async def api_model_set(request: Request):
    body = await request.json()
    return _proxy("/model", "POST", body, headers=_auth_headers(request))


@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    return _proxy("/login", "POST", body)


@app.post("/api/register")
async def api_register(request: Request):
    body = await request.json()
    return _proxy("/register", "POST", body)


@app.post("/api/logout")
async def api_logout(request: Request):
    body = await request.json()
    return _proxy("/logout", "POST", body)


@app.get("/api/me")
async def api_me(request: Request):
    auth = request.headers.get("Authorization", "")
    resp = requests.get(f"{BACKEND}/me", headers=_auth_headers(request), timeout=15)
    try:
        content = resp.json()
    except Exception:
        content = {"detail": resp.text}
    return JSONResponse(status_code=resp.status_code, content=content)


@app.post("/api/upload_file")
async def api_upload_file(request: Request):
    """转发 multipart 文件上传到后端（保留原始 body 与 Content-Type）。"""
    body = await request.body()
    headers = {"Content-Type": request.headers.get("content-type", "")}
    auth = request.headers.get("Authorization", "")
    if auth:
        headers["Authorization"] = auth
    resp = requests.post(f"{BACKEND}/upload_file", data=body, headers=headers, timeout=120)
    if resp.status_code >= 400:
        try:
            content = resp.json()
        except Exception:
            content = {"detail": resp.text}
        return JSONResponse(status_code=resp.status_code, content=content)
    return resp.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7860)
