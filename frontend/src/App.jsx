import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, Bot, User, Loader2, BookOpen, ChevronDown, ChevronUp } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your Indecimal RAG Assistant. How can I help you with our construction services today?' }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [expandedChunks, setExpandedChunks] = useState({})
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const toggleChunks = (index) => {
    setExpandedChunks(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, { question: input })
      const assistantMessage = { 
        role: 'assistant', 
        content: response.data.response,
        chunks: response.data.chunks
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error fetching response:', error)
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please make sure the backend is running.' 
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-6 py-4 shadow-sm">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold text-gray-800">Indecimal RAG Assistant</h1>
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-6">
        <div className="max-w-4xl mx-auto space-y-8">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex flex-col ${message.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`flex gap-3 max-w-[90%] sm:max-w-[80%] ${
                  message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                <div className={`mt-1 p-2 rounded-full flex-shrink-0 h-fit ${
                  message.role === 'user' ? 'bg-blue-100' : 'bg-gray-200'
                }`}>
                  {message.role === 'user' ? (
                    <User className="w-5 h-5 text-blue-600" />
                  ) : (
                    <Bot className="w-5 h-5 text-gray-600" />
                  )}
                </div>
                <div className="space-y-3 flex-1">
                  <div
                    className={`p-4 rounded-2xl shadow-sm text-sm sm:text-base ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white rounded-tr-none'
                        : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none'
                    }`}
                  >
                    <p className="whitespace-pre-wrap leading-relaxed">
                      {message.content}
                    </p>
                  </div>

                  {/* Display Chunks if they exist */}
                  {message.chunks && message.chunks.length > 0 && (
                    <div className="mt-2 w-full">
                      <button
                        onClick={() => toggleChunks(index)}
                        className="flex items-center gap-2 text-xs font-semibold text-gray-500 hover:text-blue-600 transition-colors bg-gray-100/50 px-3 py-1.5 rounded-lg border border-gray-200"
                      >
                        <BookOpen className="w-3.5 h-3.5" />
                        Retrieved Context ({message.chunks.length} chunks)
                        {expandedChunks[index] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                      </button>
                      
                      {expandedChunks[index] && (
                        <div className="mt-3 space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
                          {message.chunks.map((chunk, cIdx) => (
                            <div key={cIdx} className="bg-white border border-blue-100 rounded-xl p-4 shadow-sm relative overflow-hidden">
                              <div className="absolute top-0 left-0 w-1 h-full bg-blue-400"></div>
                              <div className="flex justify-between items-center mb-2">
                                <span className="text-[10px] font-bold text-blue-500 uppercase tracking-wider">Chunk {cIdx + 1}</span>
                                <span className="text-[10px] text-gray-400 font-medium">Source: {chunk.metadata?.source || 'Unknown'}</span>
                              </div>
                              <p className="text-xs text-gray-600 leading-relaxed italic">
                                "{chunk.content}"
                              </p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex gap-3 max-w-[75%]">
                <div className="mt-1 p-2 rounded-full bg-gray-200 flex-shrink-0">
                  <Bot className="w-5 h-5 text-gray-600" />
                </div>
                <div className="p-4 rounded-2xl bg-white border border-gray-100 rounded-tl-none flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                  <span className="text-gray-500 italic">Thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input */}
      <footer className="bg-white border-t p-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Indecimal's construction packages..."
              className="w-full pl-4 pr-12 py-3 bg-gray-100 border-none rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all outline-none"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-blue-600 disabled:text-gray-400 hover:bg-blue-50 rounded-lg transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <p className="text-center text-xs text-gray-400 mt-2">
            Powered by RAG with FastAPI and OpenRouter
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
