export async function onRequest(context) {
  return new Response(JSON.stringify({message: 'Online callback requests are not configured. Your request was not sent. Please call 978-296-8300.'}), {status: 503, headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'}});
}
