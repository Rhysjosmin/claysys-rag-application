import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const formData = await req.formData()
  
  try {
    const response = await fetch('YOUR_ACTUAL_BACKEND_URL', {
      method: 'POST',
      body: formData,
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Failed to upload document' }, { status: 500 })
  }
}

