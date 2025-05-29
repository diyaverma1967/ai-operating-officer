
export default function LoadingSpinner() {
  return (
    <div className="text-center py-4">
      <div className="w-6 h-6 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
      <p className="mt-2 text-sm text-gray-600">Thinking...</p>
    </div>
  );
}
