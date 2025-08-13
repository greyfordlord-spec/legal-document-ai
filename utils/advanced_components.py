import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Optional, Any
import json

class AdvancedAgentPanel:
    """Advanced agent panel with custom components and layouts."""
    
    def __init__(self):
        self.agents = {}
        self.layout_config = {}
    
    def create_custom_agent_card(self, agent_id: str, agent_data: Dict[str, Any]) -> str:
        """Create a custom HTML agent card with advanced styling."""
        
        html = f"""
        <div class="agent-card" id="agent-{agent_id}" 
             style="background: linear-gradient(135deg, {agent_data.get('gradient_start', '#667eea')} 0%, {agent_data.get('gradient_end', '#764ba2')} 100%);
                    border-radius: 20px;
                    padding: 2rem;
                    margin: 1rem 0;
                    color: white;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    border: 2px solid rgba(255,255,255,0.1);
                    transition: all 0.3s ease;
                    cursor: pointer;
                    position: relative;
                    overflow: hidden;">
            
            <!-- Agent Status Indicator -->
            <div style="position: absolute; top: 1rem; right: 1rem;">
                <div style="width: 12px; height: 12px; 
                            background: {agent_data.get('status_color', '#10b981')}; 
                            border-radius: 50%; 
                            border: 2px solid white;
                            box-shadow: 0 0 10px {agent_data.get('status_color', '#10b981')};">
                </div>
            </div>
            
            <!-- Agent Icon and Name -->
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 4rem; margin-bottom: 0.5rem;">{agent_data.get('icon', '🤖')}</div>
                <h3 style="margin: 0; font-size: 1.5rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    {agent_data.get('name', 'AI Agent')}
                </h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                    {agent_data.get('description', 'AI Agent Description')}
                </p>
            </div>
            
            <!-- Agent Stats -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                <div style="background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 10px; text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 700;">{agent_data.get('efficiency', '95')}%</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">Efficiency</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 10px; text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 700;">{agent_data.get('tasks', '0')}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">Active Tasks</div>
                </div>
            </div>
            
            <!-- Agent Actions -->
            <div style="display: flex; gap: 0.5rem;">
                <button onclick="manageAgent('{agent_id}')" 
                        style="flex: 1; background: rgba(255,255,255,0.2); 
                               border: 1px solid rgba(255,255,255,0.3); 
                               color: white; padding: 0.75rem; border-radius: 10px; 
                               cursor: pointer; transition: all 0.3s ease;">
                    Manage
                </button>
                <button onclick="viewLogs('{agent_id}')" 
                        style="flex: 1; background: rgba(255,255,255,0.1); 
                               border: 1px solid rgba(255,255,255,0.2); 
                               color: white; padding: 0.75rem; border-radius: 10px; 
                               cursor: pointer; transition: all 0.3s ease;">
                    Logs
                </button>
            </div>
        </div>
        
        <script>
        function manageAgent(agentId) {{
            // Send message to Streamlit
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: 'manage_' + agentId
            }}, '*');
        }}
        
        function viewLogs(agentId) {{
            // Send message to Streamlit
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: 'logs_' + agentId
            }}, '*');
        }}
        </script>
        """
        
        return html
    
    def create_agent_grid_layout(self, agents: List[Dict[str, Any]], columns: int = 3) -> None:
        """Create a responsive grid layout for agents."""
        
        # Create columns
        cols = st.columns(columns)
        
        for i, agent in enumerate(agents):
            col_idx = i % columns
            with cols[col_idx]:
                html_content = self.create_custom_agent_card(agent['id'], agent)
                components.html(html_content, height=400, scrolling=False)
    
    def create_agent_dashboard(self, agents: List[Dict[str, Any]]) -> None:
        """Create a comprehensive agent dashboard."""
        
        # Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: white; padding: 2rem; border-radius: 20px; margin: 2rem 0;
                    text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">🤖 AI Agent Command Center</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; opacity: 0.9;">
                Multi-Agent Legal Document System - Real-time Monitoring & Control
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Agents", len(agents), "Online")
        with col2:
            active_agents = sum(1 for agent in agents if agent.get('status') == 'active')
            st.metric("Active Agents", active_agents, f"+{active_agents}")
        with col3:
            total_tasks = sum(agent.get('tasks', 0) for agent in agents)
            st.metric("Total Tasks", total_tasks, "Processing")
        with col4:
            system_health = "98.5%"
            st.metric("System Health", system_health, "Optimal")
        
        # Agent Grid
        st.subheader("🤖 Agent Fleet Overview")
        self.create_agent_grid_layout(agents, 3)
        
        # Real-time Activity Feed
        st.subheader("📊 Real-time Activity Feed")
        
        # Create a container for the activity feed
        activity_container = st.container()
        
        with activity_container:
            # Simulate real-time updates
            for i, agent in enumerate(agents[:5]):  # Show last 5 activities
                with st.expander(f"🔄 {agent['name']} - Recent Activity", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Task:** {agent.get('current_task', 'Idle')}")
                        st.write(f"**Status:** {agent.get('status', 'Unknown')}")
                        st.write(f"**Last Update:** {agent.get('last_update', 'N/A')}")
                    with col2:
                        st.progress(agent.get('progress', 0) / 100)
                        st.write(f"{agent.get('progress', 0)}%")
    
    def create_agent_management_panel(self, agent_id: str, agent_data: Dict[str, Any]) -> None:
        """Create a detailed agent management panel."""
        
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 2rem; margin: 1rem 0;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1); border: 2px solid #e5e7eb;">
            <h2 style="margin: 0 0 1.5rem 0; color: #1f2937; text-align: center;">
                🎛️ {agent_data.get('name', 'Agent')} Management Panel
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Agent Configuration
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚙️ Agent Configuration")
            
            # Agent settings
            agent_name = st.text_input("Agent Name", value=agent_data.get('name', ''), key=f"name_{agent_id}")
            agent_description = st.text_area("Description", value=agent_data.get('description', ''), key=f"desc_{agent_id}")
            
            # Agent capabilities
            capabilities = agent_data.get('capabilities', [])
            st.multiselect("Capabilities", 
                          options=["Document Generation", "Legal Analysis", "Research", "Validation", "Translation"],
                          default=capabilities,
                          key=f"caps_{agent_id}")
            
            # Agent priority
            priority = st.slider("Priority Level", 1, 10, agent_data.get('priority', 5), key=f"priority_{agent_id}")
        
        with col2:
            st.subheader("📊 Performance Settings")
            
            # Performance thresholds
            efficiency_threshold = st.slider("Efficiency Threshold", 50, 100, agent_data.get('efficiency_threshold', 80), key=f"eff_thresh_{agent_id}")
            max_tasks = st.number_input("Max Concurrent Tasks", 1, 10, agent_data.get('max_tasks', 3), key=f"max_tasks_{agent_id}")
            
            # Agent behavior
            auto_restart = st.checkbox("Auto-restart on failure", value=agent_data.get('auto_restart', True), key=f"auto_restart_{agent_id}")
            load_balancing = st.checkbox("Enable load balancing", value=agent_data.get('load_balancing', True), key=f"load_balancing_{agent_id}")
        
        # Agent Actions
        st.subheader("🎯 Agent Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Restart Agent", key=f"restart_{agent_id}", use_container_width=True):
                st.success(f"Restarting {agent_data.get('name', 'Agent')}...")
        
        with col2:
            if st.button("⏸️ Pause Agent", key=f"pause_{agent_id}", use_container_width=True):
                st.warning(f"Pausing {agent_data.get('name', 'Agent')}...")
        
        with col3:
            if st.button("📊 View Metrics", key=f"metrics_{agent_id}", use_container_width=True):
                st.info(f"Loading metrics for {agent_data.get('name', 'Agent')}...")
        
        with col4:
            if st.button("🗑️ Remove Agent", key=f"remove_{agent_id}", use_container_width=True):
                st.error(f"Removing {agent_data.get('name', 'Agent')}...")
        
        # Save Configuration
        if st.button("💾 Save Configuration", key=f"save_{agent_id}", use_container_width=True):
            st.success("Configuration saved successfully!")

def create_sample_agents() -> List[Dict[str, Any]]:
    """Create sample agent data for demonstration."""
    
    return [
        {
            "id": "doc_agent_001",
            "name": "Document Agent Alpha",
            "description": "Specializes in legal document creation and formatting",
            "icon": "📋",
            "status": "active",
            "status_color": "#10b981",
            "efficiency": 95,
            "tasks": 2,
            "priority": 8,
            "gradient_start": "#667eea",
            "gradient_end": "#764ba2",
            "capabilities": ["Document Generation", "Formatting"],
            "current_task": "Generating Residential Lease",
            "progress": 75,
            "last_update": "2 minutes ago"
        },
        {
            "id": "legal_agent_001",
            "name": "Legal Compliance Agent",
            "description": "Handles legal compliance and clause validation",
            "icon": "⚖️",
            "status": "active",
            "status_color": "#3b82f6",
            "efficiency": 98,
            "tasks": 1,
            "priority": 9,
            "gradient_start": "#f093fb",
            "gradient_end": "#f5576c",
            "capabilities": ["Legal Analysis", "Validation"],
            "current_task": "Validating Contract Clauses",
            "progress": 45,
            "last_update": "1 minute ago"
        },
        {
            "id": "research_agent_001",
            "name": "Research Agent Beta",
            "description": "Conducts legal research and precedent analysis",
            "icon": "🔍",
            "status": "active",
            "status_color": "#f59e0b",
            "efficiency": 92,
            "tasks": 3,
            "priority": 7,
            "gradient_start": "#4facfe",
            "gradient_end": "#00f2fe",
            "capabilities": ["Research", "Analysis"],
            "current_task": "Researching Local Laws",
            "progress": 90,
            "last_update": "Just now"
        }
    ]

# Example usage function
def demo_advanced_agent_panel():
    """Demonstrate the advanced agent panel functionality."""
    
    st.title("🚀 Advanced Agent Panel Demo")
    
    # Create sample agents
    agents = create_sample_agents()
    
    # Initialize the advanced panel
    panel = AdvancedAgentPanel()
    
    # Create the dashboard
    panel.create_agent_dashboard(agents)
    
    # Add some interactivity
    st.subheader("🎮 Interactive Features")
    
    selected_agent = st.selectbox(
        "Select an agent to manage:",
        options=[agent['name'] for agent in agents],
        format_func=lambda x: x
    )
    
    if selected_agent:
        agent_data = next(agent for agent in agents if agent['name'] == selected_agent)
        panel.create_agent_management_panel(agent_data['id'], agent_data)

if __name__ == "__main__":
    demo_advanced_agent_panel()
