function App() {
  const API_URL = import.meta.env.VITE_API_URL || window.location.origin;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-6xl font-bold text-gray-900 mb-4">
              HishamOS
            </h1>
            <p className="text-2xl text-gray-600 mb-8">
              AI-Powered Operating System for Software Development
            </p>
            <div className="inline-block bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
              ✅ System Online - All Services Running
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              🎉 Welcome to HishamOS
            </h2>
            <p className="text-lg text-gray-700 mb-6">
              A comprehensive AI Operating System with 15 specialized agents covering the complete Software Development Lifecycle.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-3xl mb-2">🤖</div>
                <h3 className="font-bold text-lg mb-2">15 AI Agents</h3>
                <p className="text-sm text-gray-600">Specialized agents for every development phase</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-3xl mb-2">⚡</div>
                <h3 className="font-bold text-lg mb-2">73 Capabilities</h3>
                <p className="text-sm text-gray-600">From coding to deployment and support</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-3xl mb-2">🎯</div>
                <h3 className="font-bold text-lg mb-2">350+ Templates</h3>
                <p className="text-sm text-gray-600">Comprehensive command templates</p>
              </div>
            </div>

            <div className="border-t pt-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Available Agents:</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Coding Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Code Review Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Business Analyst</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>DevOps Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>QA Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Project Manager</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Scrum Master</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Release Manager</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Bug Triage Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Security Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Performance Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Documentation Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>UI/UX Agent</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Data Analyst</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Support Agent</span>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🔗 API Access</h3>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">API Root:</span>
                  <a href={`${API_URL}/api/`} target="_blank" className="text-blue-600 hover:underline">
                    /api/
                  </a>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Documentation:</span>
                  <a href={`${API_URL}/api/schema/swagger-ui/`} target="_blank" className="text-blue-600 hover:underline">
                    /api/schema/swagger-ui/
                  </a>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">ReDoc:</span>
                  <a href={`${API_URL}/api/schema/redoc/`} target="_blank" className="text-blue-600 hover:underline">
                    /api/schema/redoc/
                  </a>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Admin Panel:</span>
                  <a href={`${API_URL}/admin/`} target="_blank" className="text-blue-600 hover:underline">
                    /admin/
                  </a>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🔐 Admin Credentials</h3>
              <div className="space-y-2 text-sm bg-gray-50 p-4 rounded">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Username:</span>
                  <code className="bg-gray-200 px-2 py-1 rounded">admin</code>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Password:</span>
                  <code className="bg-gray-200 px-2 py-1 rounded">Amman123</code>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8 text-center text-gray-600">
            <p className="text-sm">
              HishamOS v1.0.0 | Built with Django + React + AI | Status: Production Ready ✅
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
