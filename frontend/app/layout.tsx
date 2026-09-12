import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "YouTube Lecture Summarizer",
  description: "Summarize YouTube lectures with AI",
};

export const viewport = {
  width: "device-width",
  initialScale: 1.0,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className="bg-gray-50">
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          <header className="bg-gradient-to-r from-gray-900 to-gray-800 text-white shadow-lg">
            <nav className="container mx-auto px-4 py-6">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold">🎓 YouTube Lecture Summarizer</h1>
                  <p className="text-gray-300 text-sm mt-1">AI-powered video summary generator</p>
                </div>
              </div>
            </nav>
          </header>

          {/* Main Content */}
          <main className="flex-1 container mx-auto px-4 py-8">
            {children}
          </main>

          {/* Footer */}
          <footer className="bg-gray-900 text-gray-300 py-6 mt-12">
            <div className="container mx-auto px-4 text-center text-sm">
              <p>
                개인정보 및 저작권: 공개 유튜브 영상의 자막만 사용하며, 저작권을 존중합니다.
              </p>
              <p className="mt-2">
                Powered by Anthropic Claude API
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
