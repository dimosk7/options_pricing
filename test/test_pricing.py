

import  pytest

from options_pricing import Option , contract_type , payoff_type , pricing_method

def test_black_scholes() :
        assert Option(42, 40, 0.1, 0.2, 6, contract_type.call, payoff_type.european).black_scholes() == pytest.approx(4.75 , abs = 0.2)
        assert Option(50 , 55, 0.05, 0.3, 6, contract_type.call, payoff_type.european).black_scholes() == pytest.approx(2.79 , abs = 0.2)
        assert Option(100 , 110, 0.08, 0.4, 12, contract_type.put, payoff_type.european).black_scholes() == pytest.approx(16.76, abs = 0.2)
        assert Option(75 , 70, 0.03, 0.2, 8, contract_type.put, payoff_type.european).black_scholes() == pytest.approx(2.15, abs = 0.2)

def test_mc_eur() :
        assert Option(42, 40, 0.1, 0.2, 6, contract_type.call, payoff_type.european).monte_carlo() == pytest.approx(4.75, abs=0.2)
        assert Option(50, 55, 0.05, 0.3, 6, contract_type.call, payoff_type.european).monte_carlo() == pytest.approx(2,79, abs=0.2)
        assert Option(100, 110, 0.08, 0.4, 12, contract_type.put, payoff_type.european).monte_carlo() == pytest.approx(16.76, abs=0.2)
        assert Option(75, 70, 0.03, 0.2, 8, contract_type.put, payoff_type.european).monte_carlo() == pytest.approx(2.15, abs=0.2)

def test_mc_asian():
        assert Option(47, 55, 0.05, 0.35, 6, contract_type.call, payoff_type.asian, 6).monte_carlo() == pytest.approx(0.59, abs=0.3)
        assert Option(45 ,50 ,0.05, 0.3, 12, contract_type.call, payoff_type.asian, 9).monte_carlo() == pytest.approx(2.47, abs=0.3)
        assert Option(100, 110, 0.08, 0.4, 12, contract_type.put, payoff_type.asian, 12).monte_carlo() == pytest.approx(12.20, abs=0.3)
        assert Option(40 ,50 ,0.05, 0.3, 12, contract_type.put, payoff_type.asian, 9).monte_carlo() == pytest.approx(9.22, abs=0.3)
