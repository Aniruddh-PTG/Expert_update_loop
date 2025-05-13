import React, { useState } from "react";

const productOwnerData = [
  { name: "BRD - User Sign Up", link: "#", status: "On Track" },
  { name: "BRD - Password Authentication", link: "#", status: "On Track" }
];

const testLeadData = [
  { name: "Test Case - User Sign Up", link: "#", status: "On Track" },
  { name: "Test Case - Validate password field", link: "#", status: "On Track" },
  { name: "Test Case - Password Authentication", link: "#", status: "On Track" }
];

const sdetData = [
  { name: "API Integration Tests", framework: "Selenium", coverage: "85%", lastRun: "Passed" }
];

const tabs = ["Product Owner", "Test Lead", "SDET"];

function Sidebar({ user }) {
  return (
    <div style={{width:220,background:'#181d26',color:'#fff',display:'flex',flexDirection:'column',justifyContent:'space-between',height:'100vh',padding:'0 0 24px 0'}}>
      <div>
        <div style={{fontWeight:700,fontSize:24,padding:'24px 0 8px 24px'}}>People<span style={{color:'#e31c24'}}>TECH GROUP</span></div>
        <div style={{padding:'8px 0 0 0'}}>
          <div style={{padding:'12px 24px',background:'#23283a',borderRadius:8,margin:'0 16px 8px 16px',fontWeight:600}}>Home</div>
          <div style={{padding:'12px 24px',margin:'0 16px',borderRadius:8}}>Settings</div>
        </div>
      </div>
      <div style={{padding:'0 24px',display:'flex',alignItems:'center'}}>
        <div style={{width:32,height:32,borderRadius:'50%',background:'#ccc',marginRight:12}}></div>
        <div>
          <div style={{fontWeight:600}}>{user}</div>
          <div style={{color:'#7bb241',fontWeight:600,fontSize:14,cursor:'pointer'}}>Sign Out</div>
        </div>
      </div>
    </div>
  );
}

function Table({ columns, data }) {
  return (
    <table style={{width:'100%',borderCollapse:'separate',borderSpacing:0,background:'#fff',borderRadius:12,overflow:'hidden',boxShadow:'0 2px 8px #0001'}}>
      <thead style={{background:'#f5f7fa'}}>
        <tr>
          {columns.map((col,i) => <th key={i} style={{padding:'12px 16px',textAlign:'left',fontWeight:700,fontSize:16}}>{col}</th>)}
        </tr>
      </thead>
      <tbody>
        {data.map((row,i) => (
          <tr key={i} style={{borderBottom:'1px solid #eee'}}>
            {Object.values(row).map((cell,j) => (
              <td key={j} style={{padding:'12px 16px',fontSize:16}}>
                {typeof cell === 'string' && cell.startsWith('http') ? <a href={cell}>Open Link</a> : cell}
              </td>
            ))}
            {data[0].status && <td style={{padding:'12px 16px'}}><span style={{background:'#eafbe7',color:'#7bb241',padding:'4px 16px',borderRadius:8,fontWeight:600}}>{row.status || row.lastRun}</span></td>}
            <td style={{padding:'12px 16px',textAlign:'center',fontSize:20}}>&#8942;</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function MainContent({ tab }) {
  if (tab === 0) {
    return (
      <div style={{flex:1,padding:'40px 40px 0 40px'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:36,fontWeight:900}}>Expert In Loop UI <span style={{fontWeight:400,color:'#bfc4d1'}}>/ Product Owner</span></div>
          <div>
            <button style={{marginRight:8,padding:'8px 20px',border:'none',borderRadius:6,background:'#e5e9f2',color:'#23283a',fontWeight:600}}>All Status</button>
            <button style={{marginRight:8,padding:'8px 20px',border:'none',borderRadius:6,background:'#eafbe7',color:'#7bb241',fontWeight:600}}>On Track</button>
            <button style={{padding:'8px 20px',border:'none',borderRadius:6,background:'#fbeee7',color:'#e3a241',fontWeight:600}}>Needs Update</button>
          </div>
        </div>
        <div style={{marginTop:32}}>
          <Table columns={["", "Product Name", "BRD ID", "Status", "Chat"]} data={productOwnerData.map(d => ({checkbox:"", name:<><span style={{display:'inline-block',width:24,height:24,background:'#bfc4d1',borderRadius:4,marginRight:8}}></span>{d.name}</>, link:<a href={d.link} style={{color:'#7bb241',textDecoration:'underline',fontWeight:600}}>Open Link</a>, status:d.status, chat:"⋮"}))} />
        </div>
      </div>
    );
  }
  if (tab === 1) {
    return (
      <div style={{flex:1,padding:'40px 40px 0 40px'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:36,fontWeight:900}}>Expert In Loop UI <span style={{fontWeight:400,color:'#bfc4d1'}}>/ Test Lead</span></div>
          <button style={{padding:'8px 20px',border:'none',borderRadius:6,background:'#e5e9f2',color:'#23283a',fontWeight:600}}>Add Test Case</button>
        </div>
        <div style={{marginTop:32}}>
          <Table columns={["", "Product Name", "Test Case ID", "Status", "Chat"]} data={testLeadData.map(d => ({checkbox:"", name:<><span style={{display:'inline-block',width:24,height:24,background:'#bfc4d1',borderRadius:4,marginRight:8}}></span>{d.name}</>, link:<a href={d.link} style={{color:'#7bb241',textDecoration:'underline',fontWeight:600}}>Open Link</a>, status:d.status, chat:"⋮"}))} />
        </div>
      </div>
    );
  }
  if (tab === 2) {
    return (
      <div style={{flex:1,padding:'40px 40px 0 40px'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:36,fontWeight:900}}>Expert In Loop UI <span style={{fontWeight:400,color:'#bfc4d1'}}>/ SDET</span></div>
          <div>
            <button style={{marginRight:8,padding:'8px 20px',border:'none',borderRadius:6,background:'#e5e9f2',color:'#23283a',fontWeight:600}}>Add Automation Suite</button>
            <button style={{padding:'8px 20px',border:'none',borderRadius:6,background:'#e5e9f2',color:'#23283a',fontWeight:600}}>Configure CI/CD</button>
          </div>
        </div>
        <div style={{marginTop:32}}>
          <Table columns={["", "Test Suite", "Framework", "Coverage", "Last Run", "Actions"]} data={sdetData.map(d => ({checkbox:"", name:<><span style={{display:'inline-block',width:24,height:24,background:'#bfc4d1',borderRadius:4,marginRight:8}}></span>{d.name}</>, framework:d.framework, coverage:d.coverage, lastRun:d.lastRun, actions:"⋮"}))} />
        </div>
      </div>
    );
  }
  return null;
}

function App() {
  const [tab, setTab] = useState(1); // Default to Test Lead
  return (
    <div style={{display:'flex',height:'100vh',background:'#f5f7fa'}}>
      <Sidebar user={tabs[tab]} />
      <div style={{flex:1,display:'flex',flexDirection:'column'}}>
        <div style={{display:'flex',justifyContent:'center',background:'#fff',borderBottom:'1px solid #e5e9f2'}}>
          {tabs.map((t,i) => (
            <button key={t} onClick={()=>setTab(i)} style={{padding:'16px 40px',fontSize:20,fontWeight:700,background:'none',border:'none',borderBottom:i===tab?'4px solid #7bb241':'4px solid transparent',color:i===tab?'#23283a':'#23283a',outline:'none',cursor:'pointer',margin:'0 8px',borderRadius:8,boxShadow:i===tab?'0 2px 8px #7bb24122':'none'}}>{t}</button>
          ))}
        </div>
        <MainContent tab={tab} />
      </div>
    </div>
  );
}

export default App; 