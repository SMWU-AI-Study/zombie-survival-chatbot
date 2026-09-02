import type { SurvivorProfile } from "../types";

interface ProfilePageProps {
    profile: SurvivorProfile;
}

function ProfilePage({ profile }: ProfilePageProps) {
    return (
        <main>
            <h1>Survivor Profile</h1>

            <h2>{profile.survivor_type}</h2>

            <p>
                추천 역할: <strong>{profile.recommended_role}</strong>
            </p>

            <section>
                <p>판단력: {profile.judgment}</p>
                <p>신중함: {profile.caution}</p>
                <p>위험 감수: {profile.risk_tolerance}</p>
                <p>협동성: {profile.cooperation}</p>
                <p>공감성: {profile.empathy}</p>
                <p>행동력: {profile.action}</p>
            </section>

            <section>
                <h3>강점</h3>
                <p>{profile.strength}</p>

                <h3>약점</h3>
                <p>{profile.weakness}</p>
            </section>
        </main>
    );
}

export default ProfilePage;