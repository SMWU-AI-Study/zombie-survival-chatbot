import TraitBar from "../components/TraitBar";
import type { SurvivorProfile } from "../types";

interface ProfilePageProps {
    profile: SurvivorProfile;
    onRestart: () => void;
}

function ProfilePage({
    profile,
    onRestart,
}: ProfilePageProps) {
    return (
        <main className="profile-page">
            <header className="profile-header">
                <span className="profile-eyebrow">
                    SURVIVOR ANALYSIS · COMPLETE
                </span>

                <p>당신의 생존 유형</p>

                <h1>{profile.survivor_type}</h1>

                <div className="role-box">
                    <span>RECOMMENDED ROLE</span>
                    <strong>{profile.recommended_role}</strong>
                </div>
            </header>

            <div className="profile-divider" />

            <section className="traits-section">
                <div className="section-heading">
                    <span>SURVIVAL TRAITS</span>
                    <small>0 — 100</small>
                </div>

                <div className="traits-grid">
                    <TraitBar
                        label="판단력"
                        value={profile.judgment}
                    />

                    <TraitBar
                        label="신중함"
                        value={profile.caution}
                    />

                    <TraitBar
                        label="위험 감수"
                        value={profile.risk_tolerance}
                    />

                    <TraitBar
                        label="협동성"
                        value={profile.cooperation}
                    />

                    <TraitBar
                        label="공감성"
                        value={profile.empathy}
                    />

                    <TraitBar
                        label="행동력"
                        value={profile.action}
                    />
                </div>
            </section>

            <section className="analysis-section">
                <article className="analysis-card strength-card">
                    <span>STRENGTH</span>
                    <p>{profile.strength}</p>
                </article>

                <article className="analysis-card weakness-card">
                    <span>WEAKNESS</span>
                    <p>{profile.weakness}</p>
                </article>
            </section>

            <div className="profile-actions">
                <button
                    className="restart-button"
                    type="button"
                    onClick={onRestart}
                >
                    다시 테스트하기
                </button>
            </div>

            <p className="profile-footer">
                ZOMBIE SURVIVAL TEST · SURVIVOR PROFILE
            </p>
        </main>
    );
}

export default ProfilePage;