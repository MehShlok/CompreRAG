"use client";
import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';

export default function Home() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        const { error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });
        if (error) {
            alert(error.message);
        } else {
            router.push('/dashboard');
        }
        setLoading(false);
    };

    const handleSignUp = async () => {
        setLoading(true);
        const { error } = await supabase.auth.signUp({
            email,
            password,
        });
        if (error) {
            alert(error.message);
        } else {
            alert('Check your email for the confirmation link!');
        }
        setLoading(false);
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
                <div className="bg-white p-8 rounded shadow-md w-full max-w-md mx-auto">
                    <h1 className="text-2xl font-bold mb-6 text-center text-black">RAG Agent Login</h1>
                    <form onSubmit={handleLogin} className="space-y-4">
                        <div>
                            <label className="block text-gray-700">Email</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full p-2 border rounded text-black"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-gray-700">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full p-2 border rounded text-black"
                                required
                            />
                        </div>
                        <div className="flex space-x-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className="flex-1 bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                            >
                                {loading ? 'Loading...' : 'Login'}
                            </button>
                            <button
                                type="button"
                                onClick={handleSignUp}
                                disabled={loading}
                                className="flex-1 bg-green-500 text-white p-2 rounded hover:bg-green-600"
                            >
                                Sign Up
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    );
}
