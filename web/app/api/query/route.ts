import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const { message } = await req.json()
  
  try {
    const response = await fetch('YOUR_ACTUAL_BACKEND_URL', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Failed to process query' }, { status: 500 })
  }
}

