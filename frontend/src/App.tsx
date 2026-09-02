import { useState } from "react";
import StartPage from "./pages/StartPage";
import ChatPage from "./pages/ChatPage";
import ProfilePage from "./pages/ProfilePage";
import type {
  ChatResponse,
  SurvivorProfile,
} from "./types";

function App() {
  const [firstScenario, setFirstScenario] =
    useState<ChatResponse | null>(null);

  const [profile, setProfile] =
    useState<SurvivorProfile | null>(null);

  if (profile) {
    return <ProfilePage profile={profile} />;
  }

  if (firstScenario) {
    return (
      <ChatPage
        firstScenario={firstScenario}
        onProfileLoaded={setProfile}
      />
    );
  }

  return <StartPage onStart={setFirstScenario} />;
}

export default App;