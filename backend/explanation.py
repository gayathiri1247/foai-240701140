def make_summary(decision, results):
    passed = sum(r["status"] == "Pass" for r in results)
    failed = sum(r["status"] == "Fail" for r in results)
    unknown = sum(r["status"] == "Not Evaluated" for r in results)
    if decision.startswith("Incomplete"):
        return f"Some information or official policy checks still need confirmation. {passed} check(s) passed, {failed} failed, and {unknown} could not be evaluated."
    if decision == "Ineligible under configured rules":
        return f"At least one configured mandatory rule failed. Review the explanations below. {passed} check(s) passed and {failed} failed."
    return f"All implemented checks passed. {unknown} bank or document check(s) remain unresolved; this is not an official lending decision."
