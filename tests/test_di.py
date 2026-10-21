from pathlib import Path
import pytest

import src.infrastructure.di.bootstrap as di
from src.infrastructure.di.inject import DependencyError, inject
from src.infrastructure.di.reflection import discover_providers
from src.infrastructure.utils.config_reader import ConfigReader
from src.infrastructure.context.vault.vault_service import VaultService
from src.infrastructure.context.sql_db.psql_dbcontext import PsqlDbContext


def test_discovery_finds_exact_singletons_without_manual_registration():
    found = discover_providers()
    for cls in (ConfigReader, VaultService, PsqlDbContext):
        assert found[cls] is cls
        assert cls.__di_singleton__ is True


def test_bootstrap_order_required():
    with pytest.raises(DependencyError, match="bootstrap_di"):
        di.resolve(ConfigReader)
    di.bootstrap_di()
    assert di.resolve(ConfigReader) is di.resolve(ConfigReader)


def test_required_injection_default_explicit_and_transient(monkeypatch):
    @inject
    class Dependency:
        def __init__(self):
            self.value = "ready"

    @inject
    class Consumer:
        def __init__(self, dependency: Dependency, optional: str = "default"):
            self.dependency = dependency
            self.optional = optional

    monkeypatch.setattr(di, "_providers", {Dependency: Dependency, Consumer: Consumer})
    monkeypatch.setattr(di, "_ready", True)
    first = di.resolve(Consumer)
    second = di.resolve(Consumer)
    assert first is not second and first.dependency is not second.dependency
    assert first.optional == "default"
    override = Dependency()
    assert Consumer(override, optional="explicit").dependency is override
    assert Consumer(override).optional == "default"


def test_unresolved_dependency_raises(monkeypatch):
    @inject
    class Missing:
        def __init__(self):
            pass

    @inject
    class NeedsMissing:
        def __init__(self, missing: Missing):
            self.missing = missing

    monkeypatch.setattr(di, "_providers", {NeedsMissing: NeedsMissing})
    monkeypatch.setattr(di, "_ready", True)
    with pytest.raises(DependencyError, match="No DI provider"):
        di.resolve(NeedsMissing)


def test_cycle_is_reported(monkeypatch):
    @inject
    class SelfDependent:
        def __init__(self, child: "SelfDependent"):
            self.child = child

    monkeypatch.setattr(di, "_providers", {SelfDependent: SelfDependent})
    monkeypatch.setattr(di, "_ready", True)
    with pytest.raises(DependencyError, match="Circular"):
        di.resolve(SelfDependent)
