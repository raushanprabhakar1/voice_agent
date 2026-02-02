import React from 'react'
import './ConversationSummary.css'

interface ConversationSummaryData {
  summary: string
  appointments_booked: any[]
  appointments_cancelled: any[]
  appointments_modified: any[]
  user_preferences: string[]
  key_points: string[]
  timestamp: string
  tool_calls: any[]
}

interface ConversationSummaryProps {
  summary: ConversationSummaryData
}

const ConversationSummary: React.FC<ConversationSummaryProps> = ({ summary }) => {
  return (
    <div className="conversation-summary">
      <h2>📋 Conversation Summary</h2>
      
      <div className="summary-section">
        <h3>Overview</h3>
        <p>{summary.summary || 'No summary available'}</p>
      </div>

      {summary.appointments_booked && summary.appointments_booked.length > 0 && (
        <div className="summary-section">
          <h3>✅ Appointments Booked</h3>
          <ul>
            {summary.appointments_booked.map((apt, index) => (
              <li key={index}>
                {apt.appointment_date} at {apt.appointment_time}
                {apt.notes && ` - ${apt.notes}`}
              </li>
            ))}
          </ul>
        </div>
      )}

      {summary.appointments_cancelled && summary.appointments_cancelled.length > 0 && (
        <div className="summary-section">
          <h3>❌ Appointments Cancelled</h3>
          <ul>
            {summary.appointments_cancelled.map((apt, index) => (
              <li key={index}>
                {apt.appointment_date} at {apt.appointment_time}
              </li>
            ))}
          </ul>
        </div>
      )}

      {summary.appointments_modified && summary.appointments_modified.length > 0 && (
        <div className="summary-section">
          <h3>✏️ Appointments Modified</h3>
          <ul>
            {summary.appointments_modified.map((apt, index) => (
              <li key={index}>
                {apt.appointment_date} at {apt.appointment_time}
              </li>
            ))}
          </ul>
        </div>
      )}

      {summary.user_preferences && summary.user_preferences.length > 0 && (
        <div className="summary-section">
          <h3>⭐ User Preferences</h3>
          <ul>
            {summary.user_preferences.map((pref, index) => (
              <li key={index}>{pref}</li>
            ))}
          </ul>
        </div>
      )}

      {summary.key_points && summary.key_points.length > 0 && (
        <div className="summary-section">
          <h3>🔑 Key Points</h3>
          <ul>
            {summary.key_points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {summary.timestamp && (
        <div className="summary-timestamp">
          Generated at: {new Date(summary.timestamp).toLocaleString()}
        </div>
      )}
    </div>
  )
}

export default ConversationSummary
