import React, { useState } from 'react';
import Login from './Login';
import TwoFactor from './TwoFactor';
import Protected from './Protected';

function App() {
    const [step, setStep] = useState(1);

    return (
        <div className='s'>
            {step === 1 && <Login setStep={setStep} />}
            {step === 2 && <TwoFactor setStep={setStep} />}
            {step === 3 && <Protected />}

        </div>
    );
}

export default App;

