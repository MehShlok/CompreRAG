"use client";
import { useState, useRef, useEffect } from 'react';
import api from '@/lib/api';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: string[];
}

export default function Chat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const response = await api.post('/query', { query: userMessage });
            const { answer, sources } = response.data;

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: answer,
                sources: sources
            }]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error processing your request.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-100">
            {/* Header */}
            <header className="bg-white shadow p-4 flex justify-between items-center">
                <h1 className="text-xl font-bold text-gray-800">RAG Agent Chat</h1>
                <Link href="/dashboard" className="text-blue-600 hover:underline">
                    Back to Dashboard
                </Link>
            </header>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-10">
                        <p>Ask a question about your documents!</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-3xl rounded-lg p-4 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-gray-800 shadow'
                            }`}>
                            {msg.role === 'user' ? (
                                <div className="whitespace-pre-wrap">{msg.content}</div>
                            ) : (
                                <div className="prose prose-sm max-w-none prose-headings:font-bold prose-p:text-gray-800 prose-li:text-gray-800 prose-strong:text-gray-900">
                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                        {msg.content}
                                    </ReactMarkdown>
                                </div>
                            )}
                            {msg.sources && msg.sources.length > 0 && (
                                <div className="mt-4 pt-4 border-t border-gray-200 text-sm">
                                    <p className="font-semibold text-gray-500 mb-2">Sources:</p>
                                    {msg.sources.map((source, i) => (
                                        <div key={i} className="bg-gray-50 p-2 rounded mb-2 text-xs text-gray-600 truncate">
                                            {source.substring(0, 150)}...
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white text-gray-800 shadow rounded-lg p-4">
                            Thinking...
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-white p-4 border-t">
                <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-4">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question..."
                        className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}
