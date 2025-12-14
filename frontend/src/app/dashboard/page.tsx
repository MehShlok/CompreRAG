"use client";
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface Document {
    id: string;
    filename: string;
    status: string;
    progress: number;
    created_at: string;
}

export default function Dashboard() {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        fetchDocuments();
        const subscription = supabase
            .channel('documents')
            .on('postgres_changes', { event: '*', schema: 'public', table: 'documents' }, (payload) => {
                console.log('Change received!', payload);
                fetchDocuments(); // Refresh list on change
            })
            .subscribe();

        return () => {
            subscription.unsubscribe();
        };
    }, []);

    const fetchDocuments = async () => {
        try {
            const { data: { session } } = await supabase.auth.getSession();
            if (!session) {
                router.push('/');
                return;
            }

            // We can fetch from backend or directly from Supabase since we have RLS
            // Let's use backend for consistency with API client setup, 
            // but direct Supabase is often faster for simple lists.
            // Using direct Supabase here for realtime simplicity.
            const { data, error } = await supabase
                .from('documents')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) throw error;
            setDocuments(data || []);
        } catch (error) {
            console.error('Error fetching documents:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Are you sure?')) return;
        try {
            await api.delete(`/documents/${id}`);
            fetchDocuments();
        } catch (error) {
            console.error('Error deleting document:', error);
            alert('Failed to delete document');
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-6xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">My Documents</h1>
                    <div className="space-x-4">
                        <Link href="/upload" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                            Upload New
                        </Link>
                        <Link href="/chat" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                            Start Chat
                        </Link>
                    </div>
                </div>

                {loading ? (
                    <p className="text-center text-gray-500">Loading...</p>
                ) : documents.length === 0 ? (
                    <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
                        No documents found. Upload one to get started!
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Filename</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">Status</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-40">Progress</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">Date</th>
                                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-32">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {documents.map((doc) => (
                                    <tr key={doc.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 text-sm font-medium text-gray-900 max-w-md truncate" title={doc.filename}>
                                            {doc.filename}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                                            <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                                doc.status === 'completed' ? 'bg-green-100 text-green-800' :
                                                doc.status === 'failed' ? 'bg-red-100 text-red-800' :
                                                'bg-yellow-100 text-yellow-800'
                                            }`}>
                                                {doc.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            <div className="w-full bg-gray-200 rounded-full h-2.5">
                                                <div className="bg-blue-600 h-2.5 rounded-full transition-all" style={{ width: `${doc.progress}%` }}></div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {new Date(doc.created_at).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                                            <button
                                                onClick={() => handleDelete(doc.id)}
                                                className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-xs font-medium transition-colors"
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
