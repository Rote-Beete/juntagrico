const subscriptionSizeSelect = document.getElementById('id_subscription_size')

const getSubscriptionSize = () => {
  return Number(
    subscriptionSizeSelect.options[
      subscriptionSizeSelect.selectedIndex
    ].getAttribute('data-units')
  )
}

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

const updateWholeContributions = () => {
  if (greenContributionInput.value) {
    greenWholeContribution.value = Number.parseFloat(
      greenContributionInput.value * getSubscriptionSize()
    ).toFixed(2)
  }
  if (yellowContributionInput.value) {
    yellowWholeContribution.value = Number.parseFloat(
      yellowContributionInput.value * getSubscriptionSize()
    ).toFixed(2)
  }
  if (redContributionInput.value) {
    redWholeContribution.value = Number.parseFloat(
      redContributionInput.value * getSubscriptionSize()
    ).toFixed(2)
  }
}

updateWholeContributions()

subscriptionSizeSelect.addEventListener('change', () => {
  updateWholeContributions()
})

greenContributionInput.addEventListener('input', (event) => {
  greenWholeContribution.value = `${event.target.value * getSubscriptionSize()}`
})

yellowContributionInput.addEventListener('input', (event) => {
  yellowWholeContribution.value = `${event.target.value * getSubscriptionSize()}`
})

redContributionInput.addEventListener('input', (event) => {
  redWholeContribution.value = `${event.target.value * getSubscriptionSize()}`
})

greenContributionInput.addEventListener('keydown', (event) => {
  if (event.key === '-') event.preventDefault()
})
yellowContributionInput.addEventListener('keydown', (event) => {
  if (event.key === '-') event.preventDefault()
})
redContributionInput.addEventListener('keydown', (event) => {
  if (event.key === '-') event.preventDefault()
})
