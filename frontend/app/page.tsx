"use client";

import React, { useState, useCallback } from "react";
import URLInput from "@/components/URLInput";
import SummarizeForm from "@/components/SummarizeForm";
import ResultDisplay from "@/components/ResultDisplay";

interface VideoInfo {
  video_id: string;
  title: string;
  channel: string;
  thumbnail_url: string;
  available_languages: string[];
  original_url: string;
}

type AppState = "input" | "form" | "result" | "loading";

export default function Home() {
  const [appState, setAppState] = useState<AppState>("input");
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null);
  const [resultData, setResultData] = useState<any>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleVideoInfoLoaded = useCallback((info: VideoInfo) => {
    setVideoInfo(info);
    setAppState("form");
    setError("");
  }, []);

  const handleSummarizing = useCallback((summarizing: boolean) => {
    if (summarizing) {
      setAppState("loading");
    }
  }, []);

  const handleSummarizeSuccess = useCallback((data: any) => {
    setResultData(data);
    setAppState("result");
  }, []);

  const handleReset = useCallback(() => {
    setVideoInfo(null);
    setResultData(null);
    setAppState("input");
    setError("");
  }, []);

  const handleError = useCallback((errorMsg: string) => {
    setError(errorMsg);
  }, []);

  return (
    <div className="max-w-4xl mx-auto">
      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm font-semibold text-red-800">❌ Error</p>
          <p className="text-red-700 mt-1">{error}</p>
        </div>
      )}

      {/* Loading State */}
      {appState === "loading" && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="flex flex-col items-center justify-center space-y-4">
              <div className="w-12 h-12 border-4 border-gray-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <p className="text-lg font-semibold text-gray-700">요약 생성 중...</p>
              <p className="text-sm text-gray-500">이 과정은 1-2분 정도 소요될 수 있습니다</p>
              <div className="w-full space-y-2 pt-4">
                <div className="flex items-center space-x-2">
                  <span className="text-green-600">✓</span>
                  <span className="text-gray-700">영상 정보 로드</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-green-600">✓</span>
                  <span className="text-gray-700">자막 가져오기</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 border-2 border-gray-300 border-t-indigo-600 rounded-full animate-spin"></div>
                  <span className="text-gray-700">Claude AI로 요약 생성 중...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Input State */}
      {appState === "input" && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">시작하기</h2>
              <p className="text-gray-600">
                유튜브 강의 링크를 입력하면 AI가 자동으로 요약을 생성합니다.
              </p>
            </div>
            <URLInput
              onVideoInfoLoaded={handleVideoInfoLoaded}
              onLoading={setIsLoading}
              onError={handleError}
              isLoading={isLoading}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <p className="font-bold text-blue-900">🎯 빠른 요약</p>
              <p className="text-sm text-blue-700 mt-1">강의의 핵심만 1-2분만에</p>
            </div>
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <p className="font-bold text-green-900">📝 구조화된 정보</p>
              <p className="text-sm text-green-700 mt-1">챕터, 용어, 퀴즈로 정리</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
              <p className="font-bold text-purple-900">⬇️ 다운로드</p>
              <p className="text-sm text-purple-700 mt-1">Markdown으로 저장 가능</p>
            </div>
          </div>

          <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
            <p className="text-sm text-yellow-800">
              <strong>⚠️ 주의:</strong> 이 서비스는 공개 유튜브 영상의 자막을 기반으로 합니다. 
              자막이 없는 영상은 요약할 수 없습니다. YouTube와 저작권자의 규정을 준수합니다.
            </p>
          </div>
        </div>
      )}

      {/* Form State */}
      {appState === "form" && videoInfo && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">요약 설정</h2>
              <p className="text-gray-600 mt-1">{videoInfo.title}</p>
            </div>
            <SummarizeForm
              videoId={videoInfo.video_id}
              videoTitle={videoInfo.title}
              availableLanguages={videoInfo.available_languages}
              onSummarizing={handleSummarizing}
              onError={handleError}
              onSuccess={handleSummarizeSuccess}
            />
          </div>
        </div>
      )}

      {/* Result State */}
      {appState === "result" && resultData && (
        <ResultDisplay
          data={resultData}
          videoId={resultData.video_id}
          onReset={handleReset}
        />
      )}
    </div>
  );
}
