--select *
--from PortfolioDB..['covid-deaths']
--order by 3, 4

--select *
--from PortfolioDB..['covid-deaths']


--select location, date, total_cases, new_cases, total_deaths, population
--from PortfolioDB..['covid-deaths']
--order by 1, 2

--select location, date, population, total_cases, (cast(total_cases as float)/cast(population as float))*100 as InfectedPercentage
--from PortfolioDB..['covid-deaths']
--order by 1, 2

--countries with high infection rates compared to population
select location, population, MAX(total_cases) as HighestInfectionCount, MAX((cast(total_cases as float)/cast(population as float))*100) as InfectedPercentage
from PortfolioDB..['covid-deaths']
group by location, population
order by InfectedPercentage desc

--countries with highest death count per pop
select continent, MAX(cast(total_deaths as int)) as TotalDeathCount
from PortfolioDB..['covid-deaths']
where continent is not null
group by continent
order by TotalDeathCount desc

--global numbers
select date, SUM(new_cases), SUM(new_deaths), (SUM(cast(total_deaths as float))/SUM(cast(total_cases as float)))*100 as deathPercentage
from PortfolioDB..['covid-deaths']
where continent is not null
group by date
order by 1, 2

--Total population vs vaccination

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
SUM(CONVERT(INT, vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioDB..['covid-deaths'] dea
join PortfolioDB..['covid-vaccinations'] vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2, 3

-- Use CTE

with PopvsVac(continent, location, date, population,new_vaccinations, RollingPeopleVaccinated)
as
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
SUM(CONVERT(INT, vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioDB..['covid-deaths'] dea
join PortfolioDB..['covid-vaccinations'] vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2, 3
)
select *, (RollingPeopleVaccinated/population)*100
from PopvsVac

--TEMP TABLE

DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric,
)

insert into #PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
SUM(CONVERT(INT, vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioDB..['covid-deaths'] dea
join PortfolioDB..['covid-vaccinations'] vac
	on dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null
--order by 2, 3

select *, (RollingPeopleVaccinated/population)*100
from #PercentPopulationVaccinated


--Creating view to store data for visualizations later

USE PortfolioDB
GO
Create View PercentPopulationVaccinated as 
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
SUM(CONVERT(INT, vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
from PortfolioDB..['covid-deaths'] dea
join PortfolioDB..['covid-vaccinations'] vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2, 3

select *
from PercentPopulationVaccinated