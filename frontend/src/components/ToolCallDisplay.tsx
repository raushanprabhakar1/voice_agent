import React, { useState, useEffect, useRef } from 'react'
import './ToolCallDisplay.css'

interface ToolCall {
  id: string
  name: string
  args: any
  result?: any
  timestamp: string
}

interface ToolCallDisplayProps {
  toolCalls: ToolCall[]
}

const ToolCallDisplay: React.FC<ToolCallDisplayProps> = ({ toolCalls }) => {
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set())
  const listRef = useRef<HTMLDivElement>(null)
  const lastToolCallIdRef = useRef<string | null>(null)


  // Auto-scroll to new tool calls and highlight them
  useEffect(() => {
    if (toolCalls.length > 0) {
      const lastCall = toolCalls[toolCalls.length - 1]
      // Only scroll if this is a new tool call (different ID)
      if (lastCall.id !== lastToolCallIdRef.current) {
        lastToolCallIdRef.current = lastCall.id
        // Scroll to bottom after a brief delay to allow DOM update
        setTimeout(() => {
          if (listRef.current) {
            listRef.current.scrollTop = listRef.current.scrollHeight
          }
        }, 100)
      }
    }
  }, [toolCalls])

  if (toolCalls.length === 0) {
    return (
      <div className="tool-call-display">
        <div className="tool-call-header-section">
          <h3>🔧 Tool Calls</h3>
          <span className="tool-call-count">0 calls</span>
        </div>
        <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
          No tool calls yet. Tool calls will appear here when the agent uses them.
        </div>
      </div>
    )
  }

  const toggleExpand = (index: number) => {
    const newExpanded = new Set(expandedItems)
    if (newExpanded.has(index)) {
      newExpanded.delete(index)
    } else {
      newExpanded.add(index)
    }
    setExpandedItems(newExpanded)
  }

  const getToolIcon = (name: string) => {
    const icons: Record<string, string> = {
      identify_user: '👤',
      fetch_slots: '📅',
      book_appointment: '✅',
      retrieve_appointments: '📋',
      cancel_appointment: '❌',
      modify_appointment: '✏️',
      end_conversation: '👋',
    }
    return icons[name] || '🔧'
  }

  const formatToolName = (name: string) => {
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      })
    } catch {
      return ''
    }
  }

  const formatArgs = (args: any) => {
    if (!args || typeof args !== 'object') return args
    // If args is a string, try to parse it
    if (typeof args === 'string') {
      try {
        return JSON.parse(args)
      } catch {
        return args
      }
    }
    return args
  }

  const formatResult = (result: any) => {
    if (!result) return null
    // If result is a string, try to parse it
    if (typeof result === 'string') {
      try {
        return JSON.parse(result)
      } catch {
        return result
      }
    }
    return result
  }

  const getResultSummary = (result: any) => {
    if (!result) return null
    const formatted = formatResult(result)
    if (formatted && typeof formatted === 'object') {
      if (formatted.error) return `Error: ${formatted.error}`
      if (formatted.success) {
        if (formatted.message) return formatted.message
        if (formatted.appointment) return `Appointment: ${formatted.appointment.appointment_date || ''} ${formatted.appointment.appointment_time || ''}`
        if (formatted.appointments && Array.isArray(formatted.appointments)) {
          return `${formatted.appointments.length} appointment(s) found`
        }
        if (formatted.slots && Array.isArray(formatted.slots)) {
          return `${formatted.slots.length} slot(s) available`
        }
        if (formatted.user) return `User: ${formatted.user.phone || ''}`
      }
    }
    return null
  }

  return (
    <div className="tool-call-display">
      <div className="tool-call-header-section">
        <h3>🔧 Tool Calls</h3>
        <span className="tool-call-count">{toolCalls.length} {toolCalls.length === 1 ? 'call' : 'calls'}</span>
      </div>
      <div className="tool-calls-list" ref={listRef}>
        {toolCalls.map((toolCall, index) => {
          const isExpanded = expandedItems.has(index)
          const formattedArgs = formatArgs(toolCall.args)
          const formattedResult = formatResult(toolCall.result)
          const resultSummary = getResultSummary(toolCall.result)
          const hasError = formattedResult && typeof formattedResult === 'object' && formattedResult.error
          
          return (
            <div 
              key={toolCall.id || index} 
              className={`tool-call-item ${hasError ? 'error' : ''} ${toolCall.result ? 'completed' : 'pending'} ${index === toolCalls.length - 1 && !toolCall.result ? 'new-call' : ''}`}
            >
              <div 
                className="tool-call-header"
                onClick={() => toggleExpand(index)}
                style={{ cursor: 'pointer' }}
              >
                <span className="tool-icon">{getToolIcon(toolCall.name)}</span>
                <span className="tool-name">{formatToolName(toolCall.name)}</span>
                <span className="tool-status">
                  {toolCall.result ? (
                    hasError ? (
                      <span className="status-error">❌ Error</span>
                    ) : (
                      <span className="status-success">✅ Success</span>
                    )
                  ) : (
                    <span className="status-pending">⏳ Processing...</span>
                  )}
                </span>
                <span className="tool-time">{formatTimestamp(toolCall.timestamp)}</span>
                <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
              </div>
              
              {resultSummary && !isExpanded && (
                <div className="tool-summary">
                  {resultSummary}
                </div>
              )}
              
              {isExpanded && (
                <div className="tool-details">
                  {formattedArgs && Object.keys(formattedArgs).length > 0 && (
                    <div className="tool-args">
                      <strong>📥 Arguments:</strong>
                      <pre>{JSON.stringify(formattedArgs, null, 2)}</pre>
                    </div>
                  )}
                  
                  {formattedResult && (
                    <div className="tool-result">
                      <strong>📤 Result:</strong>
                      {hasError ? (
                        <div className="result-error">
                          <strong>Error:</strong> {formattedResult.error}
                        </div>
                      ) : (
                        <pre>{JSON.stringify(formattedResult, null, 2)}</pre>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default ToolCallDisplay
