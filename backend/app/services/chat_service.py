from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Dict, Optional
from app.config import settings
from app.services.user_info import UserInfo, extract_user_info, HospitalUnits
from app.services.mock_policies import get_mock_policies
import json
from datetime import datetime

class GraphState(TypedDict):
    messages: List[Dict[str, str]]  # Conversation history
    current_message: str
    user_info: UserInfo
    context: str
    final_response: str
    route_decision: str

class NursingChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-4o-mini",
            streaming=True,
            temperature=0.1
        )
        self.graph = self._create_graph()
        # Store user info per conversation
        self.conversation_user_info = {}
    
    def _create_graph(self):
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("user_info_extraction", self._extract_user_info_node)
        workflow.add_node("router", self._router_node)
        workflow.add_node("get_clarification", self._clarification_node)
        workflow.add_node("context_retrieval", self._context_retrieval_node)
        workflow.add_node("generate_response", self._final_response_node)
        
        # Set entry point
        workflow.set_entry_point("user_info_extraction")
        
        # Add edges
        workflow.add_edge("user_info_extraction", "router")
        workflow.add_conditional_edges(
            "router",
            self._route_condition,
            {
                "get_clarification": "get_clarification",
                "context_retrieval": "context_retrieval"
            }
        )
        workflow.add_edge("get_clarification", END)
        workflow.add_edge("context_retrieval", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def _extract_user_info_node(self, state: GraphState) -> Dict:
        """Extract and update user information from current message"""
        # Get existing user info from conversation history
        messages = state.get("messages", [])
        conversation_key = "default"  # In production, use actual conversation_id
        
        # Get or create user info for this conversation
        if conversation_key not in self.conversation_user_info:
            self.conversation_user_info[conversation_key] = UserInfo()
        
        current_info = self.conversation_user_info[conversation_key]
        
        # Extract info from ALL previous messages, not just current
        combined_text = " ".join([msg["content"] for msg in messages if msg["role"] == "user"])
        updated_info = extract_user_info(combined_text, current_info)
        
        # Store updated info
        self.conversation_user_info[conversation_key] = updated_info
        
        return {"user_info": updated_info}
    
    def _router_node(self, state: GraphState) -> Dict:
        """Decide where to route the conversation"""
        user_info = state["user_info"]
        message = state["current_message"].lower()
        
        # Check if greeting or intro
        greetings = ["hi", "hello", "hey", "help", "how does this work"]
        if any(greeting in message for greeting in greetings) and len(message) < 50:
            return {"route_decision": "get_clarification"}
        
        # Check if user info is incomplete
        if not user_info.is_complete():
            return {"route_decision": "get_clarification"}
        
        # Check if question is too vague
        question_words = ["what", "how", "when", "where", "why", "can", "should"]
        if not any(word in message for word in question_words) or len(message) < 10:
            return {"route_decision": "get_clarification"}
        
        return {"route_decision": "context_retrieval"}
    
    def _route_condition(self, state: GraphState) -> str:
        return state["route_decision"]
    
    def _clarification_node(self, state: GraphState) -> Dict:
        """Help user clarify their request"""
        user_info = state["user_info"]
        message = state["current_message"]
        
        # Create clarification prompt
        if not user_info.unit and not user_info.role:
            clarification_prompt = f"""
User message: "{message}"

You are helping a nurse clarify their request. They haven't provided their unit or role yet.

Respond with:
1. Brief acknowledgment of their message
2. Ask them to provide their unit and role
3. Be friendly and helpful

Example: "Hi! I'd be happy to help you with nursing policies. To provide the most accurate information, could you please tell me your role (e.g., Nurse, Tech) and which unit you work in (e.g., ICU, ED)?"
"""
        elif not user_info.unit:
            clarification_prompt = f"""
User message: "{message}"
User role: {user_info.role}

The user has provided their role but not their unit. Ask them for their specific unit.
"""
        elif not user_info.role:
            clarification_prompt = f"""
User message: "{message}"
User unit: {user_info.unit}

The user has provided their unit but not their role. Ask them for their specific role.
"""
        else:
            clarification_prompt = f"""
User message: "{message}"
User info: {user_info.role} in {user_info.unit}

The user's question is unclear or too vague. Help them clarify what specific policy or procedure they're asking about. Be helpful and guide them to ask a more specific question.
"""
        
        messages = [HumanMessage(content=clarification_prompt)]
        response = self.llm.invoke(messages)
        
        return {"final_response": response.content}
    
    def _context_retrieval_node(self, state: GraphState) -> Dict:
        """Retrieve relevant policies for the user's question"""
        user_info = state["user_info"]
        question = state["current_message"]
        
        # Get mock policies
        policies = get_mock_policies(user_info.unit, question)
        
        # Format context
        context = "\n\n".join([
            f"**{policy['title']}**\n{policy['content']}\n{policy['unit_specific']}"
            for policy in policies
        ])
        
        return {"context": context}
    
    def _final_response_node(self, state: GraphState) -> Dict:
        """Generate final response with context"""
        user_info = state["user_info"]
        question = state["current_message"]
        context = state["context"]
        
        response_prompt = f"""
### USER'S CURRENT INFO ###
UNIT: {user_info.unit}
ROLE: {user_info.role}

### USER'S QUESTION ###
{question}

### CONTEXT ###
{context}

You are a helpful nursing assistant. Answer the user's question based on the provided context. 
- Be specific and practical
- Reference the unit-specific information when relevant
- If the context doesn't fully answer their question, say so
- Keep responses professional but friendly
"""
        
        messages = [HumanMessage(content=response_prompt)]
        response = self.llm.invoke(messages)
        
        return {"final_response": response.content}
    
    async def chat(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Process a chat message through the graph"""
        if conversation_history is None:
            conversation_history = []
        
        # Add current message to history
        conversation_history.append({"role": "user", "content": message})
        
        # Create initial state
        initial_state = {
            "messages": conversation_history,
            "current_message": message,
            "user_info": UserInfo(),
            "context": "",
            "final_response": "",
            "route_decision": ""
        }
        
        # Run graph
        result = await self.graph.ainvoke(initial_state)
        response = result["final_response"]
        
        # Add response to history
        conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    async def chat_stream(self, message: str, conversation_history: List[Dict[str, str]] = None):
        """Stream the final response after graph processing"""
        if conversation_history is None:
            conversation_history = []
        
        # Add current message to history
        conversation_history.append({"role": "user", "content": message})
        
        # Create initial state
        initial_state = {
            "messages": conversation_history,
            "current_message": message,
            "user_info": UserInfo(),
            "context": "",
            "final_response": "",
            "route_decision": ""
        }
        
        # Run graph up to final response
        result = await self.graph.ainvoke(initial_state)
        
        # If it went to clarification, just return that
        if "final_response" in result and result["final_response"]:
            for char in result["final_response"]:
                yield char
            return
        
        # Otherwise stream the final response
        user_info = result["user_info"]
        context = result.get("context", "")
        
        response_prompt = f"""
### USER'S CURRENT INFO ###
UNIT: {user_info.unit}
ROLE: {user_info.role}

### USER'S QUESTION ###
{message}

### CONTEXT ###
{context}

You are a helpful nursing assistant. Answer the user's question based on the provided context. 
- Be specific and practical
- Reference the unit-specific information when relevant
- If the context doesn't fully answer their question, say so
- Keep responses professional but friendly
"""
        
        messages = [HumanMessage(content=response_prompt)]
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                yield chunk.content
