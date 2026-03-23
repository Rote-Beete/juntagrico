const greenContributionInput = document.getElementById(
  'id_green_contribution_amount'
)

const yellowContributionInput = document.getElementById(
  'id_yellow_contribution_amount'
)

const redContributionInput = document.getElementById(
  'id_red_contribution_amount'
)

const greenWholeContribution = document.getElementById('id_green_whole_amount')

const yellowWholeContribution = document.getElementById(
  'id_yellow_whole_amount'
)
const redWholeContribution = document.getElementById('id_red_whole_amount')

greenContributionInput.addEventListener('input', (event) => {
  greenWholeContribution.value = `${event.target.value}`
})

yellowContributionInput.addEventListener('input', (event) => {
  yellowWholeContribution.value = `${event.target.value}`
})

redContributionInput.addEventListener('input', (event) => {
  redWholeContribution.value = `${event.target.value}`
})
