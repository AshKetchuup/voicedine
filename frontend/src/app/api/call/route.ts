
import { NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(req: Request) {
    try {
        const { phone_number, restaurant_name } = await req.json();

        const apiKey = process.env.BLAND_API_KEY || process.env.NEXT_PUBLIC_BLAND_API_KEY;

        if (!apiKey) {
            console.error('Missing BLAND_API_KEY');
            return NextResponse.json(
                { error: 'Server configuration error: Missing API Key' },
                { status: 500 }
            );
        }

        if (!phone_number || !restaurant_name) {
            return NextResponse.json(
                { error: 'Missing phone_number or restaurant_name' },
                { status: 400 }
            );
        }

        // Default voice ID (British Male)
        const voiceId = "1";

        const payload = {
            phone_number: "+447466348530",
            task: `
        You are a personal assistant named James. 
        Call ${restaurant_name} and ask to book a table for 4 people at 8pm tonight.
        You are polite but firm. 
        If they say yes, say "Fantastic, see you then" and hang up.
        If they say no, ask "Do you have anything later, maybe 9pm?"
      `,
            // voice: voiceId,
            language: "en-GB",
            record: true,
            max_duration: 3, // Limit call duration for testing/cost
        };

        console.log(`>> INITIATING CALL TO ${restaurant_name} (${phone_number})`);

        const response = await axios.post('https://api.bland.ai/v1/calls', payload, {
            headers: {
                'authorization': apiKey,
                'Content-Type': 'application/json',
            },
        });

        console.log(">> CALL DISPATCHED. ID:", response.data.call_id);
        return NextResponse.json(response.data);

    } catch (error: any) {
        console.error("Call failed:", error.response?.data || error.message);
        return NextResponse.json(
            { error: error.response?.data?.message || 'Failed to initiate call' },
            { status: error.response?.status || 500 }
        );
    }
}
